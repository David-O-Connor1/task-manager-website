# Task Manager Website

A task management web application built with Flask that allows users to register, log in, and manage their own tasks. The application supports full CRUD functionality, session management, flash messages, and user authorization.

---

## Features

* User registration
* User login and logout
* Session management
* Flash messages
* Add tasks
* View tasks
* Edit tasks
* Mark tasks as complete
* Delete tasks
* User authorization (users can only access their own tasks)
* Template inheritance with Jinja
* SQLite database integration

---

## Technologies Used

* Python
* Flask
* SQLite
* WTForms
* Flask-Session
* Werkzeug Security
* HTML
* CSS

---

## Project Structure

```
task-manager-website/
│
├── app.py
├── database.py
├── forms.py
├── schema.sql
├── requirements.txt
├── app.db
├── .gitignore
│
├── templates/
│   ├── layout.html
│   ├── index.html
│   ├── register.html
│   ├── login.html
│   ├── dashboard.html
│   ├── add_task.html
│   └── edit_task.html
│
└── static/
    └── styles.css
```

---

## Installation

Clone the repository:

```
git clone https://github.com/David-O-Connor1/task-manager-website.git
```

Move into the project directory:

```
cd task-manager-website
```

Create a virtual environment:

```
python -m venv .venv
```

Activate the virtual environment:

### Windows

```
.venv\Scripts\activate
```

### macOS / Linux

```
source .venv/bin/activate
```

Install dependencies:

```
pip install -r requirements.txt
```

Run the application:

```
python -m flask run
```

Open your browser and navigate to:

```
http://127.0.0.1:5000
```

---

## Concepts Demonstrated

* Flask routing
* Template inheritance
* Forms with WTForms
* Input validation
* Session management
* Authentication
* Authorization
* Password hashing
* SQLite databases
* Foreign keys
* CRUD operations
* Flash messages
* Jinja templates
* Git and GitHub workflow

---

## Author

**David O'Connor**

Built as part of a personal Flask and Python backend development portfolio.
