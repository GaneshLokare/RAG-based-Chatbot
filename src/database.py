import sqlite3
from hashlib import sha256

DB_FILE = "app_data.db"  # SQLite database file


def create_database():
    """Initialize the SQLite database and create necessary tables."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS indexes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            index_name TEXT NOT NULL,
            user_id INTEGER,
            FOREIGN KEY (user_id) REFERENCES users (id)
        )
    """)
    conn.commit()
    conn.close()


def hash_password(password):
    """Hash a password using SHA-256."""
    return sha256(password.encode()).hexdigest()


def validate_user(username, password):
    """Validate user credentials."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE username = ? AND password = ?", (username, hash_password(password)))
    user = cursor.fetchone()
    conn.close()
    return user[0] if user else None


def register_user(username, password):
    """Register a new user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hash_password(password)))
        conn.commit()
    except sqlite3.IntegrityError:
        return False  # Username already exists
    conn.close()
    return True


def get_user_indexes(user_id):
    """Retrieve all index names for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT index_name FROM indexes WHERE user_id = ?", (user_id,))
    indexes = [row[0] for row in cursor.fetchall()]
    conn.close()
    return indexes


def save_index(user_id, index_name):
    """Save an index name for a user."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO indexes (index_name, user_id) VALUES (?, ?)", (index_name, user_id))
    conn.commit()
    conn.close()