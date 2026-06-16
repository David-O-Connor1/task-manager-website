from flask import Flask,render_template,redirect,url_for,session,g,request,flash
from forms import RegistrationForm,LoginForm,add_taskForm
from database import get_db,close_db
from werkzeug.security import generate_password_hash,check_password_hash
from flask_session import Session
from functools import wraps

app = Flask(__name__)
app.teardown_appcontext(close_db)
app.config["SECRET_KEY"] = "my_secret_key"
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.before_request
def load_logged_in_user():
    g.user = session.get("user_id",None)

def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if g.user is None:
            flash("Please log in to access that page","error")
            return redirect(url_for("login",next = request.url))
        return view(*args, **kwargs)
    return wrapped_view

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/dashboard")
@login_required
def dashboard():
    db = get_db()
    tasks = db.execute("""SELECT * FROM tasks WHERE user_id = ?""",(g.user,)).fetchall()
    return render_template("dashboard.html",tasks=tasks)

@app.route("/register",methods=["GET","POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        db = get_db()
        conflict = db.execute("""SELECT * FROM users WHERE username = ?""",(user,)).fetchone()

        if conflict is not None:
            form.user.errors.append("Username conflicts with another")
        else:
            db.execute("""INSERT INTO users(username,password) VALUES (?, ?)""",(user,generate_password_hash(password)))
            db.commit()
            flash("Registration successful! Please log in","success")
            return redirect(url_for("login"))
    return render_template("register.html",form=form)

@app.route("/login",methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = form.user.data
        password = form.password.data
        db = get_db()
        matching_user = db.execute("""SELECT * FROM users WHERE username = ?""",(user,)).fetchone()
        if matching_user is None:
            form.user.errors.append("Unknown user id")
        elif not check_password_hash(matching_user["password"],password):
            form.password.errors.append("Incorrect password")
        else:
            session.clear()
            session["user_id"] = matching_user["id"]
            flash("Logged in successfully!","success")
            next_page = request.args.get("next")
            if not next_page:
                next_page = url_for("home")
            return redirect(next_page)
    return render_template("login.html",form=form)

@app.route("/logout")
@login_required
def logout():
    session.clear()
    flash("You have been logged out","success")
    return redirect(url_for("home"))

@app.route("/add_task",methods=["GET","POST"])
@login_required
def add_task():
    form = add_taskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data

        db = get_db()
        db.execute("""INSERT INTO tasks(title, description, completed, user_id) 
                   VALUES(?, ?, ?, ?)""",(title,description,0,g.user))
        db.commit()
        return redirect(url_for("dashboard"))
    return render_template("add_task.html",form=form)

@app.route("/complete_task/<int:task_id>")
@login_required
def complete_task(task_id):
    db = get_db()
    db.execute("""UPDATE tasks SET completed = 1 WHERE id = ? AND user_id = ?""",(task_id,g.user))
    db.commit()
    return redirect(url_for("dashboard"))

@app.route("/delete_task/<int:task_id>")
@login_required
def delete_task(task_id):
    db = get_db()
    db.execute("""DELETE FROM tasks WHERE id = ? AND user_id = ?""",(task_id,g.user))
    db.commit()
    return redirect(url_for("dashboard"))

@app.route("/edit_task/<int:task_id>",methods = ["GET","POST"])
@login_required
def edit_task(task_id):
    db = get_db()
    task = db.execute("""SELECT * FROM tasks WHERE id = ? and user_id = ?""",(task_id,g.user)).fetchone()
    if task is None:
        flash("Task either doesn't exist or is owned by another user","error")
        return redirect(url_for("dashboard"))

    form = add_taskForm()
    if form.validate_on_submit():
        title = form.title.data
        description = form.description.data
        db.execute("""UPDATE tasks SET title = ?, description = ? WHERE id = ? and user_id = ?""",(title,description,task_id,g.user))
        db.commit()
        flash("Task updated!","success")
        return redirect(url_for("dashboard"))

    if request.method == "GET":
        form.title.data = task["title"]
        form.description.data = task["description"]
    return render_template("edit_task.html",form=form)
    

    