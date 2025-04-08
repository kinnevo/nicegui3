from nicegui import app
from database import user_db

def is_authenticated() -> bool:
    """Check if the user is authenticated."""
    return app.storage.user.get('authenticated', False)

def get_current_user_role() -> str:
    """Get the current user's role."""
    return app.storage.user.get('role', 'user')

def get_current_user_data() -> dict:
    """Get the current user's data."""
    username = app.storage.user.get('username')
    if username:
        return user_db.get_user(username) or {}
    return {}

def login_user(username: str, password: str) -> bool:
    """Log in a user."""
    if user_db.verify_user(username, password):
        app.storage.user['authenticated'] = True
        app.storage.user['username'] = username
        app.storage.user['role'] = 'user'  # Default role
        return True
    return False

def logout() -> None:
    """Log out the current user."""
    app.storage.user.clear()
    app.storage.browser.clear() 