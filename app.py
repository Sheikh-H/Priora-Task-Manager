from services.auth import login_required, login_user, create_user
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
    current_app,
    abort,
)
from flask_wtf.csrf import CSRFProtect, CSRFError
from services.config import initialise
from flask_session import Session
from datetime import timedelta
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
    PERMANENT_SESSION_LIFETIME=timedelta(minutes=15),
)


app.config["SESSION_TYPE"] = "filesystem"
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

Session(app)

csrf = CSRFProtect(app)


@app.after_request
def security_headers(response):
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; " "script-src 'self'"
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
            login = {"email": email, "password": password}
            user, message = login_user(login)
            if user:
                session.clear()
                session.permanent = True
                session["user-id"] = user["id"]
                flash(message, "success")
                return redirect(url_for("account"))
    return render_template("user/login.html", title=title, description=description)


@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get("user-id"):
        return redirect(url_for("account"))
    description = "Sign up page"
    title = "Register an account"
    if request.method == "POST":
        fname = request.form.get("fname", "").strip()
        sname = request.form.get("sname", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        confirm_password = request.form.get("confirm-password", "").strip()
        if fname and sname and email and password and confirm_password:
            new_user = {
                "fname": fname,
                "sname": sname,
                "email": email,
                "password": confirm_password,
            }
            user, message = create_user(new_user)
            if user:
                session.clear()
                session.permanent = True
                flash(message, "success")
                session["user-id"] = user["id"]
                return redirect(url_for("account"))
            else:
                flash(message, "error")

    return render_template("user/register.html", title=title, description=description)


@app.route("/user/home", methods=["GET", "POST"])
@login_required
def account():
    title = "Welcome Back!"
    return render_template("user/home.html", title=title)


@app.route("/logout", methods=["POST"])
@login_required
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
