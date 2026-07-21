import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()


def connect_database():
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
                               "username"	TEXT NOT NULL,
                               "password"	TEXT NOT NULL,
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
