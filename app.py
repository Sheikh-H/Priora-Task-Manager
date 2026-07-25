from services.tasks import (
    load_tasks,
    search_task_by_id,
    search_tasks_by_date,
    search_upcoming_tasks,
    mark_as_complete,
    search_overdue_tasks,
)
from services.auth import (
    login_required,
    login_user,
    create_user,
    password_reset,
    password_change,
    password_reset_required,
)
from flask import (
    Flask,
    current_app,
    render_template,
    send_from_directory,
    url_for,
    redirect,
    request,
    session,
    flash,
    Response,
    abort,
)
from services.database import (
    find_task_by_id,
    find_user_by_id,
    get_task_logs,
    get_all_task_logs,
    add_log,
    update_task_fields,
    delete_task_by_id,
    add_new_task,
    get_all_tasks,
    get_completed_tasks,
    get_incomplete_tasks,
)
from flask_wtf.csrf import CSRFProtect, CSRFError
from datetime import timedelta, datetime
from services.config import initialise
from flask_session import Session
from dotenv import load_dotenv
import os

load_dotenv()

initialise()

app = Flask(__name__)


app.config["TEMPLATES_AUTO_RELOAD"] = True


app.config.update(
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_SAMESITE="LAX",
    PERMANENT_SESSION_LIFETIME=timedelta(hours=1),
)


app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Session(app)

csrf = CSRFProtect(app)


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; "
        "script-src 'self'; "
        "style-src 'self' https://fonts.googleapis.com; "
        "font-src 'self' https://fonts.gstatic.com;"
    )
    return response


@app.route("/", methods=["GET"])
def home():
    description = "This is the home page"
    return render_template("main/home.html", description=description)


@app.route("/about")
def about():
    description = "This is the about page"
    title = "About"
    return render_template("main/about.html", description=description, title=title)


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("user-id"):
        return redirect(url_for("account"))
    description = "Login page"
    title = "Login"
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        if email and password:
            logins = {"email": email, "password": password}
            user, message = login_user(logins)
            if user:
                session.clear()
                session.permanent = True
                session["user-id"] = user["user_id"]
                flash(message, "success")
                return redirect(url_for("account"))
            else:
                flash(message, "error")
    return render_template("user/login.html", title=title, description=description)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user-id"):
        return redirect(url_for("account"))
    description = "Sign up page"
    title = "Register an account"
    if request.method == "POST":
        fname = request.form.get("fname", "").strip().lower()
        sname = request.form.get("sname", "").strip().lower()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm-password", "").strip()
        memorable = request.form.get("memorable-info", "").strip().lower()
        if fname and sname and email and password and confirm_password and memorable:
            new_user = {
                "fname": fname,
                "sname": sname,
                "email": email,
                "password": confirm_password,
                "memorable": memorable,
            }
            user, message = create_user(new_user)
            if user:
                session.clear()
                session.permanent = True
                flash(message, "success")
                session["user-id"] = user["user_id"]
                return redirect(url_for("account"))
            else:
                flash(message, "error")
    return render_template("user/register.html", title=title, description=description)


@app.route("/reset-password", methods=["GET", "POST"])
def reset_password():
    title = "Password Reset"
    description = "Reset your password on Priora"
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        memorable = request.form.get("memorable-info", "").strip().lower()
        user = {"email": email, "memorable": memorable}
        user_changed, message = password_reset(user)
        if user_changed:
            session.clear()
            session.permanent = True
            session["user-id"] = user_changed["id"]
            flash(message, "success")
            return redirect(url_for("change_password"))
        else:
            flash(message, "error")
    return render_template(
        "user/forgot-password.html", title=title, description=description
    )


@app.route("/change-password", methods=["GET", "POST"])
@login_required
def change_password():
    title = "Change password"
    if request.method == "POST":
        new_password = request.form.get("password", "").strip()
        conf_password = request.form.get("confirm-password", "").strip()
        if new_password != conf_password:
            flash("Password mismatch", "error")
            return redirect(url_for("change_password"))
        success, message = password_change(session.get("user-id"), conf_password)
        if success:
            flash(message, "success")
            return redirect(url_for("account"))
        flash(message, "error")
        return redirect(url_for("change_password"))
    return render_template("/user/change-password.html", title=title)


@app.route("/user/home", methods=["GET", "POST"])
@login_required
@password_reset_required
def account():
    title = "Welcome Back!"
    user = find_user_by_id(session.get("user-id"))
    new_user = bool(user["new_user"])
    tasks = load_tasks(user)

    date = datetime.now().replace(microsecond=0).date()

    today = date
    tomorrow = date + timedelta(days=1)
    future = date + timedelta(days=2)

    todays = search_tasks_by_date(today, user)
    tomorrows = search_tasks_by_date(tomorrow, user)
    upcoming = search_upcoming_tasks(future, user)
    overdue = search_overdue_tasks(today, user)

    if request.method == "POST":
        task_id = request.form.get("task-id")
        update = mark_as_complete(task_id, user)
        if update:
            flash(update, "success")
            return redirect(url_for("account"))
        return redirect(url_for("account"))

    return render_template(
        "user/home.html",
        title=title,
        tasks=tasks,
        new_user=new_user,
        todays=todays,
        tomorrows=tomorrows,
        upcoming=upcoming,
        user=user,
        overdue=overdue,
    )


@app.route("/user/tasks/add-task", methods=["GET", "POST"])
@login_required
@password_reset_required
def add_task():
    title = "Add a new task"
    user = find_user_by_id(session.get("user-id"))
    task = {}
    if request.method == "POST":
        task_title = request.form.get("title", "").strip().lower()
        task_description = request.form.get("description", "").strip().lower()
        due_date = request.form.get("due-date", "").strip()
        due_time = request.form.get("due-time", "").strip()
        date = datetime.now().replace(microsecond=0)
        today = f"{date.date()}"
        if due_date < today:
            flash("Please enter a valid date!", "error")
            return redirect(url_for("add_task"))
        if not task_title:
            flash("Enter a task title!", "error")
            return redirect(url_for("add_task"))

        if len(task_title) > 20:
            flash("Title must be under 20 characters!", "error")
            return redirect(url_for("add_task"))

        task["title"] = task_title
        task["description"] = task_description
        task["due_date"] = due_date
        task["due_time"] = due_time

        success = add_new_task(user, **task)
        if success:
            flash("Task added!", "success")
            return redirect(url_for("account"))
        flash("Unable to add task!", "error")
        return redirect(url_for("add_task"))

    return render_template("tasks/add-task.html", title=title)


@app.route("/user/tasks/tomorrow", methods=["GET", "POST"])
@login_required
@password_reset_required
def tomorrows_tasks():
    title = "Tomorrows Tasks"
    date = datetime.now().replace(microsecond=0).date()
    date = date + timedelta(days=1)
    user = find_user_by_id(session.get("user-id"))
    new_user = bool(user["new_user"])
    if new_user:
        return redirect(url_for("account"))
    tasks = search_tasks_by_date(date, user)
    return render_template("tasks/tomorrows-tasks.html", title=title, tasks=tasks)


@app.route("/user/task/<int:task_id>", methods=["GET", "POST"])
@login_required
@password_reset_required
def task(task_id):
    user = find_user_by_id(session.get("user-id"))
    task = search_task_by_id(task_id, user)
    title = f"{task['title']}"
    logs = get_task_logs(task_id, user)
    date = datetime.now().replace(microsecond=0).date()
    today = f"{date}"
    overdue = bool(task["due_date"] < today)
    return render_template(
        "tasks/task-page.html",
        title=title,
        task=task,
        logs=logs,
        overdue=overdue,
        today=today,
    )


@app.route("/user/task/<int:task_id>/log", methods=["GET"])
@login_required
@password_reset_required
def all_logs(task_id):
    user = find_user_by_id(session.get("user-id"))
    logs = get_all_task_logs(task_id, user)
    return render_template("tasks/task-log.html", logs=logs)


@app.route("/user/task/<int:task_id>/complete", methods=["POST"])
@login_required
@password_reset_required
def task_complete(task_id):
    user = find_user_by_id(session.get("user-id"))
    task = find_task_by_id(task_id, user["user_id"])
    completed = bool(task["completed"])
    success = mark_as_complete(task_id, user)
    if success and not completed:
        flash("Task marked as complete!", "success")
        return redirect(url_for("task", task_id=task_id))
    if success and completed:
        flash("Task marked as incomplete!", "success")
        return redirect(url_for("task", task_id=task_id))
    flash("Unable to update task", "error")
    return redirect(url_for("task", task_id=task_id))


@app.route("/user/task/<int:task_id>/add-log", methods=["POST"])
@login_required
@password_reset_required
def add_task_log(task_id):
    user = find_user_by_id(session.get("user-id"))
    comment = request.form.get("comment")
    update = add_log(task_id, user, comment)
    if update:
        flash("Task log added!", "success")
    else:
        flash("Unable to add log", "error")
    return redirect(url_for("task", task_id=task_id))


@app.route("/user/task/<int:task_id>/delete", methods=["post"])
@login_required
@password_reset_required
def delete_task(task_id):
    user = find_user_by_id(session.get("user-id"))
    success = delete_task_by_id(task_id, user)
    if success:
        flash("Task deleted successfully!", "success")
        return redirect(url_for("account"))
    flash("Unable to delete task!", "error")
    return redirect(url_for("task", task_id=task_id))


@app.route("/user/task/<int:task_id>/update", methods=["POST"])
@login_required
@password_reset_required
def update_task(task_id):
    user = find_user_by_id(session.get("user-id"))
    task = find_task_by_id(task_id, user["user_id"])
    title = request.form.get("title", "").strip().lower()
    description = request.form.get("description", "").strip().lower()
    due_date = request.form.get("due-date")
    due_time = request.form.get("due-time")
    updates = {}
    if task["title"].lower() != title.lower():
        updates["title"] = title
    if task["description"].lower() != description.lower():
        updates["description"] = description
    if due_date:
        try:
            datetime.strptime(due_date, "%Y-%m-%d").date()
            if task["due_date"] < due_date:
                flash("Please enter a valid date")
            if task["due_date"] != due_date:
                updates["due_date"] = due_date
        except (ValueError, TypeError):
            flash("Please enter a valid date!", "error")
    if due_time:
        try:
            datetime.strptime(due_time, "%H:%M").time()
            if task["due_time"] != due_time:
                updates["due_time"] = due_time
        except (ValueError, TypeError):
            flash("Please enter a valid time!", "error")
    success = update_task_fields(task_id, user, **updates)
    if success:
        flash("Task updated successfully!", "success")
        return redirect(url_for("task", task_id=task_id))
    flash("Unable to update task!", "error")
    return redirect(url_for("task", task_id=task_id))


@app.route("/logout", methods=["POST"])
@login_required
@password_reset_required
def logout():
    session.clear()
    flash("Logout successful!", "success")
    return redirect(url_for("home"))


@app.route("/robots.txt")
def robots():
    if current_app.static_folder is None:
        abort(404)
    return send_from_directory(current_app.static_folder, "robots.txt")


@app.route("/sitemap.xml")
def sitemap():
    xml = f"""<?xml version="1.0" encoding="UTF-8"?>
    <urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <url>
        <loc>{request.url_root}</loc>
    </url>
    <url>
        <loc>{request.url_root}about</loc>
    </url>
    <url>
        <loc>{request.url_root}login</loc>
    </url>
    <url>
        <loc>{request.url_root}register</loc>
    </url>
    </urlset>
    """
    return Response(xml, mimetype="application/xml")


@app.errorhandler(CSRFError)
def csrf_error(error):
    return render_template("error/400.html", reason=error.description), 400


@app.errorhandler(403)
def forbidden(error):
    return render_template("error/403.html"), 403


@app.errorhandler(404)
def not_found(error):
    return render_template("error/404.html"), 404


@app.errorhandler(400)
def bad_request(error):
    return render_template("error/400.html"), 400


@app.errorhandler(500)
def server_error(error):
    return render_template("error/500.html"), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
