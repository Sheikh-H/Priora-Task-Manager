from services.database import insert_user, find_user
from flask import session, redirect, url_for
from argon2 import PasswordHasher
from dotenv import load_dotenv
from functools import wraps
import secrets
import os

load_dotenv()

hasher = PasswordHasher()


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user-id") is None:
            return redirect(url_for("login"))
        return f(*args, **kwargs)

    return decorated_function


def create_user(new_user):
    existing_user = find_user(new_user["email"])
    if existing_user:
        return False, "Existing user!"
    try:
        hashed_password = hasher.hash(new_user["password"])
        new_user["password"] = hashed_password
        user = insert_user(new_user)
        return user, "Account created!"
    except Exception as e:
        print(e)
        return False, "Unable to create account!"


def login_user(logins):
    user = find_user(logins["email"])
    if user:
        try:
            hasher.verify(user["password"], logins["password"])
            return user, "User loggin successful!"
        except Exception as e:
            print(e)
            return False, "Incorrect Password!"
    else:
        return False, "No account, please register!"


def generate_secrets():
    secret = secrets.token_hex(32)
    text = f"SECRET_KEY={secret}\n"
    if not os.path.exists(".env"):
        with open(".env", "w") as f:
            f.write(text)
    else:
        with open(".env", "r") as f:
            contents = f.read()
        if "SECRET_KEY=" not in contents:
            with open(".env", "a") as f:
                f.write(text)
        else:
            key = ""
            for line in contents.splitlines():
                if line.startswith("SECRET_KEY="):
                    key = line
                    break
            value = key.split("=", 1)[1].strip()
            if not value:
                updated_contents = ""
                for line in contents.splitlines():
                    if line.startswith("SECRET_KEY="):
                        updated_contents += f"SECRET_KEY={secret}\n"
                    else:
                        updated_contents += line + "\n"
                with open(".env", "w") as f:
                    f.write(updated_contents)
