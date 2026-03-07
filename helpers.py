from functools import wraps
from flask import redirect, session


def login_required(f):
    """
    Decorate routes to require login.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def skill_level_label(level):
    """
    Convert numeric level to human-readable label.
    """
    if level <= 5:
        return "Beginner"
    elif level <= 10:
        return "Intermediate"
    else:
        return "Advanced"


def get_role_label(skills):
    """
    Decide whether user is Frontend / Backend / Fullstack
    based on skill distribution.
    """
    frontend_points = 0
    backend_points = 0

    for skill in skills:
        if skill["category"] == "frontend":
            frontend_points += skill["level"]
        elif skill["category"] == "backend":
            backend_points += skill["level"]

    total = frontend_points + backend_points

    if total == 0:
        return "New Developer"

    frontend_ratio = frontend_points / total
    backend_ratio = backend_points / total

    # Mostly frontend
    if frontend_ratio >= 0.7:
        return "Frontend Student" if frontend_points < 15 else "Frontend Specialist"

    # Mostly backend
    if backend_ratio >= 0.7:
        return "Backend Student" if backend_points < 15 else "Backend Pro"

    # Balanced
    return "Full-Stack Developer"