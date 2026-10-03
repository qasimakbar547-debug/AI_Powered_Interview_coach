import sqlite3
import bcrypt
from datetime import datetime

DATABASE_NAME = "interview_coach.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            score REAL NOT NULL,
            total_questions INTEGER NOT NULL,
            date TEXT NOT NULL,
            report TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    """)

    conn.commit()
    conn.close()


def create_user(name, email, password):
    conn = get_connection()
    cursor = conn.cursor()

    hashed_password = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt()
    ).decode("utf-8")

    try:
        cursor.execute("""
            INSERT INTO users
            (name, email, password, created_at)
            VALUES (?, ?, ?, ?)
        """, (
            name,
            email,
            hashed_password,
            datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        ))

        conn.commit()
        user_id = cursor.lastrowid
        conn.close()

        return True, user_id

    except sqlite3.IntegrityError:
        conn.close()
        return False, None


def login_user(email, password):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, name, email, password
        FROM users
        WHERE email = ?
    """, (email,))

    user = cursor.fetchone()
    conn.close()

    if user:
        user_id, name, email, stored_password = user

        if bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8")
        ):
            return {
                "id": user_id,
                "name": name,
                "email": email
            }

    return None


def save_interview(
    user_id,
    category,
    score,
    total_questions,
    report
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO interviews
        (user_id, category, score, total_questions, date, report)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (
        user_id,
        category,
        score,
        total_questions,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        report
    ))

    conn.commit()
    conn.close()


def get_interview_history(user_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, category, score, total_questions, date, report
        FROM interviews
        WHERE user_id = ?
        ORDER BY id DESC
    """, (user_id,))

    history = cursor.fetchall()
    conn.close()

    return history