from services.auth import login_user, create_user
from flask import Flask, render_template, url_for, redirect, request, session, flash
from services.config import initialise
from flask_wtf.csrf import CSRFProtect
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
    description = "Login page"
    title = "Login"
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "").strip()
        success = login_user(email, password)
    return render_template("user/login.html", title=title, description=description)


@app.route("/register", methods=["GET", "POST"])
def register():
    description = "Sign up page"
    title = "Register an account"
    return render_template("user/register.html", title=title, description=description)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
