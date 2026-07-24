from argon2 import PasswordHasher
from dotenv import load_dotenv
from datetime import datetime
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
	                        "user_id"	INTEGER NOT NULL UNIQUE,
	                        "first_name"	TEXT NOT NULL,
	                        "last_name"	TEXT NOT NULL,
                            "email"	TEXT NOT NULL UNIQUE,
                            "password"	TEXT NOT NULL,
                            "memorable"	TEXT NOT NULL,
                            "date_created"	TEXT NOT NULL,
                            "reset"	INTEGER NOT NULL DEFAULT 0,
                            "new_user"	INTEGER NOT NULL DEFAULT 1,
                            PRIMARY KEY("user_id" AUTOINCREMENT)
                            );
                            """)
        connection.commit()
        connection.execute("""
                        CREATE TABLE IF NOT EXISTS "tasks" (
                            "task_id"	INTEGER NOT NULL UNIQUE,
                            "user_id"	INTEGER NOT NULL,
                            "title"	TEXT NOT NULL,
                            "description"	TEXT NOT NULL,
                            "due_date"	TEXT NOT NULL,
                            "due_time"	TEXT NOT NULL,
                            "completion_date"	TEXT,
                            "completion_time"	TEXT,
                            "completed"	INTEGER NOT NULL DEFAULT 0,
                            PRIMARY KEY("task_id" AUTOINCREMENT),
                            FOREIGN KEY("user_id") 
                                REFERENCES "users"("user_id")
                                ON DELETE CASCADE
                            );""")
        connection.commit()
        connection.execute("""
                        CREATE TABLE IF NOT EXISTS "task_logs" (
                            "log_id"	INTEGER NOT NULL UNIQUE,
                            "task_id"	INTEGER NOT NULL,
                            "user_id"   INTEGER NOT NULL,
                            "date"	TEXT NOT NULL,
                            "time"	TEXT NOT NULL,
                            "comment"	TEXT NOT NULL,
                            PRIMARY KEY("log_id" AUTOINCREMENT),
                            FOREIGN KEY("task_id") 
                                REFERENCES "tasks"("task_id")
                                ON DELETE CASCADE,
                            FOREIGN KEY ("user_id")
                                REFERENCES "users"("user_id")
                                ON DELETE CASCADE
                            );""")
        connection.commit()
        connection.execute("""
                        CREATE INDEX IF NOT EXISTS idx_tasks_user
                        ON tasks(user_id);
                        """)
        connection.execute("""
                        CREATE INDEX IF NOT EXISTS idx_tasks_completed
                        ON tasks(completed);
                        """)
        connection.execute("""
                        CREATE INDEX IF NOT EXISTS idx_tasks_due_date
                        ON tasks(due_date);
                        """)
        connection.execute("""
                        CREATE INDEX IF NOT EXISTS idx_task_logs_task
                        ON task_logs(task_id);
                        """)
        connection.execute("""
                        CREATE INDEX IF NOT EXISTS idx_task_logs_user
                        ON task_logs(user_id);
                        """)
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
        now = datetime.now().replace(microsecond=0)
        cursor.execute(
            """INSERT INTO users (first_name, last_name, email, password, memorable, date_created) VALUES (?,?,?,?,?,?);""",
            (
                user["fname"],
                user["sname"],
                user["email"],
                user["password"],
                user["memorable"],
                f"{now}",
            ),
        )
        connection.commit()
        user = find_user_by_email(user["email"])
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
            """SELECT * FROM users WHERE user_id = ?;""",
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
            """UPDATE users SET password = ?, reset = 0 WHERE user_id = ?""",
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
            """SELECT reset FROM users WHERE user_id = ?;""",
            (user_id,),
        )
        required = cursor.fetchone()
        if required and required["reset"] == 1:
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def all_tasks(user):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM tasks WHERE user_id = ?;""",
            (user["user_id"],),
        )
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
