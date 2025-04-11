import sqlite3
from datetime import datetime
import hashlib
from typing import Optional, Dict, Any
from nicegui import app

class UserDB:
    def __init__(self, db_path: str = 'visit_sv.db'):
        self.db_path = db_path
        self._init_db()

    def _init_db(self):
        """Initialize the database with the conversations table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS conversations (
                    session_id TEXT PRIMARY KEY,
                    username TEXT NOT NULL,
                    save_time TEXT NOT NULL,
                    conversation_history TEXT,
                    FOREIGN KEY (username) REFERENCES users(username)
                )
            ''')
            conn.commit()

    def create_conversation(self, session_id: str, username: str, conversation_history: str) -> bool:
        """Create a new conversation record."""
        try:
            current_time = datetime.now().isoformat()
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO conversations (session_id, username, save_time, conversation_history)
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

def save_db():
    session_id = app.storage.browser['session_id']
    username = app.storage.user.get('username', 'Unknown User')
    conversation = str(app.storage.browser['conversation_history'])
    
    # Try to update first
    if not user_db.update_conversation(session_id, conversation):
        # If update fails, create new conversation
        user_db.create_conversation(session_id, username, conversation) 