from codeop import compile_command
from datetime import datetime, timedelta
from argon2 import PasswordHasher
from dotenv import load_dotenv
from datetime import datetime
from flask import flash
import sqlite3
import os

from flask.cli import F

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


def find_tasks_before_date(date, user_id):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM tasks WHERE completed = 0 AND user_id = ? and due_date < ? ORDER BY due_date ASC, due_time ASC LIMIT 5;""",
            (user_id, date),
        )
        tasks = cursor.fetchall()
        return tasks
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
        return bool(required and required["reset"] == 1)
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
            """SELECT * FROM tasks WHERE user_id = ? AND completed = 0;""",
            (user["user_id"],),
        )
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def find_task_by_id(task_id, user_id):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM tasks WHERE task_id = ? AND user_id = ?;""",
            (task_id, user_id),
        )
        task = cursor.fetchone()
        return task
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def find_tasks_by_date(date, user_id):
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM tasks WHERE user_id = ? AND due_date = ? AND completed = 0 ORDER BY due_date ASC, due_time ASC LIMIT 10;""",
            (user_id, date),
        )
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def find_tasks_after_date(date_from, user_id):
    connection = connect_database()
    cursor = connection.cursor()

    try:
        cursor.execute(
            """SELECT * FROM tasks WHERE user_id = ? AND due_date >= ? AND completed = 0 ORDER BY due_date ASC , due_time ASC LIMIT 10;""",
            (user_id, date_from),
        )
        tasks = cursor.fetchall()
        return tasks
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def toggle_task_complete(task_id, user_id):
    task = find_task_by_id(task_id, user_id)
    connection = connect_database()
    cursor = connection.cursor()
    date = datetime.now().replace(microsecond=0)
    day = date.date()
    time = date.time()
    day = f"{day}"
    time = f"{time}"
    if task:
        try:
            if task["completed"]:
                cursor.execute(
                    """UPDATE tasks SET completed = 0 WHERE user_id = ? AND task_id = ?""",
                    (user_id, task_id),
                )
                connection.commit()

                cursor.execute(
                    """INSERT INTO task_logs (date, time, comment, user_id, task_id) VALUES (?,?,?,?,?);""",
                    (day, time, "Task marked as incomplete", user_id, task_id),
                )
                connection.commit()
                return True
            else:
                cursor.execute(
                    """UPDATE tasks SET completed = 1, completion_date = ?, completion_time = ? WHERE user_id = ? AND task_id = ?""",
                    (day, time, user_id, task_id),
                )
                connection.commit()
                cursor.execute(
                    """INSERT INTO task_logs (date, time, comment, user_id, task_id) VALUES (?,?,?,?,?);""",
                    (day, time, "Task marked as complete", user_id, task_id),
                )
                connection.commit()
                return True
        except Exception as e:
            print(e)
            return False
        finally:
            connection.close()


def get_task_logs(task_id, user):
    user_id = user["user_id"]
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM task_logs WHERE task_id = ? AND user_id = ? ORDER BY date DESC, time DESC LIMIT 5;""",
            (task_id, user_id),
        )
        logs = cursor.fetchall()
        return logs
    except Exception as e:
        print(e)
        return None
    finally:
        connection.close()


def get_all_task_logs(task_id, user):
    user_id = user["user_id"]
    connection = connect_database()
    cursor = connection.cursor()
    try:
        cursor.execute(
            """SELECT * FROM task_logs WHERE task_id = ? AND user_id = ? ORDER BY date DESC, time DESC;""",
            (task_id, user_id),
        )
        logs = cursor.fetchall()
        return logs
    except Exception as e:
        print(e)
        return None
    finally:
        connection.close()


def add_log(task_id, user, comment):
    user_id = user["user_id"]
    connection = connect_database()
    cursor = connection.cursor()
    date = datetime.now().replace(microsecond=0)
    today = date.date()
    time = date.time()
    today = f"{today}"
    time = f"{time}"
    try:
        cursor.execute(
            """INSERT INTO task_logs (task_id, user_id, comment, date, time) VALUES (?, ?, ?, ?, ?);""",
            (task_id, user_id, comment, today, time),
        )
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()


def update_task_fields(task_id, user, **updates):
    user_id = user["user_id"]
    connection = connect_database()
    cursor = connection.cursor()

    title = updates.get("title")
    description = updates.get("description")
    date = updates.get("due_date")
    time = updates.get("due_time")

    log_entry = ""

    try:
        if title:
            log_entry += f"Title update to: {title}"
            cursor.execute(
                """UPDATE tasks SET title = ? WHERE task_id = ? AND user_id = ? """,
                (title, task_id, user_id),
            )

        if description:
            log_entry += f"Description updated to: {description}"
            cursor.execute(
                """UPDATE tasks SET description = ? WHERE task_id = ? AND user_id = ? """,
                (description, task_id, user_id),
            )

        if date:
            log_entry += f"Due date updated to: {date}"
            cursor.execute(
                """UPDATE tasks SET due_date = ? WHERE task_id = ? AND user_id = ? """,
                (date, task_id, user_id),
            )

        if time:
            log_entry += f"Due time updated to: {time}"
            cursor.execute(
                """UPDATE tasks SET due_time = ? WHERE task_id = ? AND user_id = ? """,
                (time, task_id, user_id),
            )

        connection.commit()
    except Exception as e:
        print(e)
        return False
    if log_entry:
        add_log(task_id, user, log_entry)
        return True
    return False


def delete_task_by_id(task_id, user):
    connection = connect_database()
    cursor = connection.cursor()
    user_id = user["user_id"]
    try:
        cursor.execute(
            """DELETE FROM tasks WHERE task_id = ? AND user_id = ?;""",
            (task_id, user_id),
        )
        connection.commit()
        return True
    except Exception as e:
        print(e)
        return False
    finally:
        connection.close()
