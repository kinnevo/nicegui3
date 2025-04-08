from nicegui import ui, app
from datetime import datetime
import uuid
import secrets
from pages.list import list_page
  

@ui.page('/')
def home():
    with ui.column().classes('w-full items-center'):
        ui.label('Home').classes('text-h3 q-mb-md')
        ui.label('Welcome to SV Exploration!').classes('text-h5 q-mb-md')
        ui.label(f"{app.storage.general['titulo']}").classes('text-h3 q-mb-md')
    with ui.row().classes('w-full items-center'):
        ui.button('Page 1').classes('text-h3 q-mb-md').on_click(lambda: ui.navigate.to('/page1'))

@ui.page('/page1')
def page_one():
    list_page()
      
@app.on_shutdown
def shutdown():
    # This code runs when the app is shutting down
    print("Application is shutting down...")
    # Clean up resources, close connections, etc.
    # Cleanup code here
    pass

@app.on_startup
def on_startup():
    # Initialize storage
    app.storage.general['user_list'] = {}

    if not hasattr(app.storage.general, 'titulo'):
        app.storage.general['titulo'] = "TITULO 123"
    
    # Initialize other app state
    if not hasattr(app.storage.general, 'logged_users'):
        app.storage.general['logged_users'] = {}
    
    # Initialize list_of_users
    if not hasattr(app.storage.general, 'list_of_users'):
        app.storage.general['list_of_users'] = {}
    
    # Set up any other required resources
    # Initialize databases, load configs, etc.


secret_key = secrets.token_hex(32)
ui.run(title='SV Exploration', port=8080, favicon='static/favicon.svg', storage_secret=secret_key) 



