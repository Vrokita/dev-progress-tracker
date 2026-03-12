Dev Progress Tracker

Video Demo: https://youtu.be/FNJ8juKOoJg

⸻
s
Description

Dev Progress Tracker is a web application that allows users to track their learning progress while studying programming and computer science topics.

The main idea behind this project is that programming progress should be measured by completed work, not by vague self-assessment. Instead of manually assigning skill levels, users log completed projects and select the programming languages and tools used for each project. The application then automatically calculates skill progression and determines an overall developer profile.

This project was created as the Final Project for CS50: Introduction to Computer Science.

⸻

Motivation

While learning programming, it is common to study multiple languages and technologies at the same time. However, it can be difficult to clearly see progress or identify areas of focus. Many learners either underestimate or overestimate their abilities because there is no structured way to visualize what they have actually worked on.

Dev Progress Tracker solves this problem by focusing on project-based progress tracking. Each completed project contributes to one or more skills, and those skills are grouped into broader categories such as frontend and backend development. This allows the application to dynamically infer the user’s learning direction and experience level over time.

⸻

Features
	•	User registration and login with password hashing
	•	Secure session-based authentication
	•	Add completed projects with a title and description
	•	Select multiple programming languages or tools per project
	•	Automatic skill progression based on project submissions
	•	Skill level classification:
	•	Beginner (levels 0–5)
	•	Intermediate (levels 6–10)
	•	Advanced (levels 11+)
	•	Dynamic developer role calculation:
	•	Frontend-oriented
	•	Backend-oriented
	•	Full-stack
	•	Generalist
	•	Dashboard overview showing progress and profile title
	•	Project history page listing all submitted projects and associated skills
	•	Persistent data storage using SQLite

⸻

How the Application Works

Project-Based Progress Tracking

Users do not manually increase skill counters. Instead, they submit completed projects and explicitly select the skills used in each project. A single project can be associated with multiple skills (for example, HTML, CSS, and JavaScript).

The application stores the relationship between projects and skills in the database. Skill progression is calculated dynamically by counting how many projects reference each skill. This approach avoids inconsistencies and ensures accurate tracking even if projects are later edited or removed.

⸻

Developer Role Calculation

The application determines an overall developer role by analyzing the balance between frontend and backend skills.
	•	Frontend skills include technologies such as HTML, CSS, and JavaScript
	•	Backend skills include technologies such as Python, SQL, and Flask

If the user’s completed projects strongly favor one category, the application assigns a frontend or backend profile. If progress is balanced across both categories, the user is classified as full-stack. The experience level (Beginner, Intermediate, Advanced) is determined by the total number of recorded skill usages.

⸻

Database Design

The application uses SQLite and consists of the following tables:
	•	users
	•	Stores registered users and hashed passwords
	•	projects
	•	Stores user-submitted projects and metadata
	•	skills
	•	Stores available programming languages and tools
	•	project_skills
	•	Junction table linking projects to skills (many-to-many relationship)

This database structure allows a single project to contribute to multiple skills and keeps the system flexible and scalable.

File Structure

    progress-tracker/
    │
    ├── app.py               # Main Flask application
    ├── helpers.py           # Helper functions and reusable logic
    ├── database.db          # SQLite database
    ├── requirements.txt     # Python dependencies
    ├── README.md            # Project documentation
    │
    ├── templates/            # HTML templates
    │   ├── layout.html
    │   ├── login.html
    │   ├── register.html
    │   ├── dashboard.html
    │   ├── add_project.html
    │   └── history.html
    │
    └── static/
        ├── styles.css        # CSS styling
        └── script.js         # Optional JavaScript

Technologies Used

	•	Python
	•	Flask
	•	SQLite
	•	HTML
	•	CSS
	•	Werkzeug (for password hashing)

How to Run the Project
	1.	Install the required dependencies:
        pip install -r requirements.txt

    2.	Run the Flask application:
        flask run

    3.	Open a web browser and navigate to:
        http://127.0.0.1:5000

Acknowledgements

    This project was created as the Final Project for CS50: Introduction to Computer Science by Harvard University. It applies concepts learned throughout the course, including Python programming, SQL databases, web development with Flask, and relational database design.
    
