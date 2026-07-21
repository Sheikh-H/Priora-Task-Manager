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


@app.route("/create_user", methods=["GET", "POST"])
def create_user():
    title = "Create New User"
    description = "This is the create new user page - priora"
    return render_template("", title=title, description = description)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
