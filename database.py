import sqlite3
from datetime import datetime
import hashlib
from typing import Optional, Dict, Any

class UserDB:
    def __init__(self, db_path: str = 'users.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with the users table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    username TEXT PRIMARY KEY,
                    password TEXT NOT NULL,
                    name TEXT NOT NULL,
                    last_name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    role TEXT NOT NULL,
                    creation_date TEXT NOT NULL,
                    last_access TEXT NOT NULL
                )
            ''')
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    session_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    start_time TEXT NOT NULL,
                    end_time TEXT,
                    conversation_history TEXT,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')
            conn.commit()

    def _hash_password(self, password: str) -> str:
        """Hash the password using SHA-256."""
        return hashlib.sha256(password.encode()).hexdigest()

    def create_user(self, username: str, password: str, name: str, last_name: str, email: str, role: str = 'user') -> bool:
        """Create a new user in the database."""
        try:
            hashed_password = self._hash_password(password)
            current_time = datetime.now().isoformat()
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (username, password, name, last_name, email, role, creation_date, last_access)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', (username, hashed_password, name, last_name, email, role, current_time, current_time))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username: str, password: str) -> bool:
        """Verify user credentials."""
        hashed_password = self._hash_password(password)
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT password FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result and result[0] == hashed_password:
                # Update last access time
                cursor.execute('''
                    UPDATE users 
                    SET last_access = ? 
                    WHERE username = ?
                ''', (datetime.now().isoformat(), username))
                conn.commit()
                return True
        return False

    def get_user(self, username: str) -> Optional[Dict[str, Any]]:
        """Get user information by username."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
            result = cursor.fetchone()
            if result:
                return dict(result)
        return None

    def update_last_access(self, username: str) -> None:
        """Update the last access time for a user."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE users 
                SET last_access = ? 
                WHERE username = ?
            ''', (datetime.now().isoformat(), username))
            conn.commit()

    def create_conversation(self, session_id: str, username: str, conversation_history: str) -> bool:
        """Create a new conversation record."""
        try:
            current_time = datetime.now().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations (session_id, username, start_time, conversation_history)
                    VALUES (?, ?, ?, ?)
                ''', (session_id, username, current_time, conversation_history))
                conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def update_conversation(self, session_id: str, conversation_history: str) -> bool:
        """Update an existing conversation with new history."""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE conversations 
                    SET conversation_history = ? 
                    WHERE session_id = ?
                ''', (conversation_history, session_id))
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def end_conversation(self, session_id: str) -> bool:
        """Mark a conversation as ended."""
        try:
            end_time = datetime.now().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE conversations 
                    SET end_time = ? 
                    WHERE session_id = ?
                ''', (end_time, session_id))
                conn.commit()
            return True
        except sqlite3.Error:
            return False

    def get_conversation(self, session_id: str) -> Optional[Dict[str, Any]]:
        """Get conversation details by session_id."""
        with sqlite3.connect(self.db_path) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM conversations WHERE session_id = ?', (session_id,))
            result = cursor.fetchone()
            if result:
                return dict(result)
        return None

# Create a global instance
user_db = UserDB() 