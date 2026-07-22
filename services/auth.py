from argon2 import PasswordHasher
from dotenv import load_dotenv
from services.database import insert_user, find_user
import secrets
import os

load_dotenv()

hasher = PasswordHasher()


def create_user(user):
    try:
        hashed_password = hasher(user["password"])
        user["password"] = hashed_password
        success = insert_user(user)
        return success
    except Exception as e:
        print(e)
        return False


def login_user(email, password):
    user = find_user(email)
    if user:
        try:
            hasher.verify(user["password"], password)
            return user
        except Exception as e:
            print(e)
            return False
    else:
        return False


def generate_secrets():
    secret = secrets.token_hex(32)
    text = f"\nSECRET_KEY={secret}\n"
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
