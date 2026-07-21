from flask import Flask, render_template, url_for, redirect
from flask_session import Session
from datetime import timedelta
from dotenv import load_dotenv
from services.database import initialise_database
import secrets
import os

load_dotenv()

initialise_database()

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


@app.route("/", methods=["GET"])
def home():
    description = "This is the home page"
    return render_template("main/home.html", description=description)


@app.route("/about")
def about():
    description = "This is the about page"
    title = "About"
    return render_template("main/about.html", description=description, title=title)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
