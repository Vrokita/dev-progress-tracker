from flask import Flask, render_template, request, redirect, session
from flask_session import Session
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from helpers import login_required, get_role_label

app = Flask(__name__)

# Configure session
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

DATABASE = "progress.db"


def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def dashboard():
    db = get_db()

    skills = db.execute(
        "SELECT name, category, level FROM skills WHERE user_id = ?",
        (session["user_id"],)
    ).fetchall()

    projects = db.execute(
        "SELECT COUNT(*) FROM projects WHERE user_id = ?",
        (session["user_id"],)
    ).fetchone()[0]

    role = get_role_label(skills)

    return render_template(
        "dashboard.html",
        skills=skills,
        projects=projects,
        role=role
    )


@app.route("/add_project", methods=["GET", "POST"])
@login_required
def add_project():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        tools = request.form.getlist("tools")

        db = get_db()

        # Save project
        db.execute(
            "INSERT INTO projects (user_id, title, description) VALUES (?, ?, ?)",
            (session["user_id"], title, description)
        )

        # Update skills
        for tool in tools:
            skill = db.execute(
                "SELECT level FROM skills WHERE user_id = ? AND name = ?",
                (session["user_id"], tool)
            ).fetchone()

            if skill:
                db.execute(
                    "UPDATE skills SET level = level + 1 WHERE user_id = ? AND name = ?",
                    (session["user_id"], tool)
                )
            else:
                category = "frontend" if tool in ["HTML", "CSS", "JavaScript"] else "backend"
                db.execute(
                    "INSERT INTO skills (user_id, name, category, level) VALUES (?, ?, ?, 1)",
                    (session["user_id"], tool, category)
                )

        db.commit()
        return redirect("/")

    return render_template("add_project.html")


@app.route("/history")
@login_required
def history():
    db = get_db()

    projects = db.execute(
        "SELECT title, description, created_at FROM projects WHERE user_id = ? ORDER BY created_at DESC",
        (session["user_id"],)
    ).fetchall()

    return render_template("history.html", projects=projects)


@app.route("/login", methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        db = get_db()
        user = db.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        if user and check_password_hash(user["hash"], password):
            session["user_id"] = user["id"]
            return redirect("/")

        return render_template("login.html", error="Invalid credentials")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            return render_template("register.html", error="Missing username or password")

        hash_pw = generate_password_hash(password)

        db = get_db()

        try:
            db.execute(
                "INSERT INTO users (username, hash) VALUES (?, ?)",
                (username, hash_pw)
            )
            db.commit()
        except sqlite3.IntegrityError:
            return render_template("register.html", error="Username already taken")

        return redirect("/login")

    return render_template("register.html")


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")