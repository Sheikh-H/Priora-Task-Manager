from argon2 import PasswordHasher
from dotenv import load_dotenv
from sqlalchemy import insert
from services.database import insert_user

load_dotenv()

hasher = PasswordHasher().hash

def create_user(user):
    try:
        hashed_password = hasher(user['password'])
        user['password'] = hashed_password
        success = insert_user(user)
        return success
    except Exception as e:
        print(e)
        return False