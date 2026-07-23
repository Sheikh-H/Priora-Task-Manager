from dotenv import load_dotenv
from argon2 import PasswordHasher
import sqlite3
import os

load_dotenv()

hasher = PasswordHasher()


def connect_database():
    os.makedirs("instance", exist_ok=True)
    connection = sqlite3.connect("instance/task-manager.db")
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON;")
    return connection


def initialise_database():
    connection = connect_database()
    try:
        connection.execute("""
                        CREATE TABLE IF NOT EXISTS "users" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "first_name"	TEXT NOT NULL,
                            "last_name"	TEXT NOT NULL,
                            "email"	TEXT NOT NULL UNIQUE,
                            "password"	TEXT NOT NULL,
                            "memorable"	TEXT NOT NULL,
                            "reset"	INTEGER NOT NULL DEFAULT 0,
                            PRIMARY KEY("id" AUTOINCREMENT)
                            );
                            """)
        connection.commit()

        connection.execute("""
                        CREATE TABLE IF NOT EXISTS "tasks" (
                            "id"	INTEGER NOT NULL UNIQUE,
                            "user_id"	INTEGER NOT NULL,
                            "title"	TEXT NOT NULL,
                            "description"	TEXT NOT NULL,
                            "due_date"	TEXT NOT NULL,
                            "due_time"	TEXT NOT NULL,
                            "completion_date"	TEXT NOT NULL,
                            "completion_time"	INTEGER NOT NULL,
                            "completed"	INTEGER NOT NULL DEFAULT 0,
                            PRIMARY KEY("id" AUTOINCREMENT),
                            FOREIGN KEY("user_id") 
                            REFERENCES "users"("id")
                            ON DELETE CASCADE
                            );""")
        connection.commit()
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def insert_user(user):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """INSERT INTO users (first_name, last_name, email, password, memorable) VALUES (?,?,?,?,?);""",
            (
                user["fname"],
                user["sname"],
                user["email"],
                user["password"],
                user["memorable"],
            ),
        )
        connection.commit()
        user = find_user(user["email"])
        return user
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def find_user_by_email(email):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM users WHERE email = ?;""",
            (email,),
        )
        user = cursor.fetchone()
        if user:
            return user
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def find_user_by_id(user_id):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM users WHERE id = ?;""",
            (user_id,),
        )
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def reset_password(user):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """UPDATE users SET reset = 1 WHERE email = ?;""",
            (user["email"],),
        )
        connection.commit()
        cursor.execute(
            """SELECT * FROM users WHERE email = ?;""",
            (user["email"],),
        )
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def password_update(user_id, password):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """UPDATE users SET password = ?, reset = 0 WHERE id = ?""",
            (password, user_id),
        )
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def is_reset_req(user_id):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT reset FROM users WHERE id = ?;""",
            (user_id,),
        )
        required = cursor.fetchone()
        if required == 1:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
