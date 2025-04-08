from nicegui import ui, app
import requests
import json
from datetime import datetime
import os
from typing import List, Optional
import uuid
from dotenv import load_dotenv
from auth import is_authenticated, logout, get_current_user_role
from database import user_db


#example of linkk
#        ui.link('Share Your Dreams', '/chat').props('flat color=primary')


# Load environment variables
load_dotenv()

# LangFlow connection settings
BASE_API_URL = os.environ.get("BASE_API_URL")
FLOW_ID = os.environ.get("FLOW_ID")
APPLICATION_TOKEN = os.environ.get("APPLICATION_TOKEN")
ENDPOINT = os.environ.get("ENDPOINT")

def run_flow(message: str, history: Optional[List[dict]] = None) -> dict:
    """Run the LangFlow with the given message and conversation history."""
    api_url = f"{BASE_API_URL}/api/v1/run/{ENDPOINT}"
    
    # Get the current session ID and username from storage
    session_id = app.storage.browser.get('session_id', str(uuid.uuid4()))
    username = app.storage.user.get('username', 'User')
    
    if history and len(history) > 0:
        formatted_history = json.dumps(history)
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "conversation_history": formatted_history,
            "user": username,
            "session_id": session_id
        }
    else:
        payload = {
            "input_value": message,
            "output_type": "chat",
            "input_type": "chat",
            "user": username,
            "session_id": session_id
        }

    headers = {"Authorization": f"Bearer {APPLICATION_TOKEN}", "Content-Type": "application/json"}
    
    try:
        response = requests.post(api_url, json=payload, headers=headers)
        response_data = response.json()
        return response_data
    except Exception as e:
        raise e

@ui.page('/chat')
def chat_page():
    # if not is_authenticated():
    #     ui.navigate.to('/login')
    #     return

    # # Initialize session if not exists
    # if not app.storage.browser.get('session_id'):
    #     new_session_id = str(uuid.uuid4())
    #     print(f"Initial session created with ID: {new_session_id}")
    #     app.storage.browser['session_id'] = new_session_id
    #     app.storage.browser['conversation_history'] = []
    #     # Create initial conversation record
    #     username = app.storage.user.get('username')
    #     if username:
    #         user_db.create_conversation(
    #             new_session_id,
    #             username,
    #             str([])
    #         )

    # # Create a left drawer that's always visible
    # with ui.left_drawer(fixed=True, bordered=True).classes('bg-gray-100'):
    #     ui.label('Navigation').classes('text-h6 q-mb-md')
        
    #     # Authentication section
    #     if is_authenticated():
    #         ui.label(f'Logged in as: {app.storage.user.get("username")}')
    #         ui.button('Logout', on_click=lambda: (logout(), ui.navigate.to('/'))).props('flat color=negative')
    #         ui.link('User Functions', '/user-functions').props('flat color=primary')
    #         ui.link('Home', '/').props('flat color=primary')
            
    #         # Show admin link only to admin users
    #         if get_current_user_role() == 'admin':
    #             ui.link('Admin Functions', '/admin-functions').props('flat color=warning')
    #     else:
    #         ui.button('Login', on_click=lambda: ui.navigate.to('/login')).props('flat color=primary')
        
    #     ui.separator()
        
    #     # Session management
    #     if is_authenticated():
    #         def new_session():
    #             # Save current conversation to database
    #             current_history = app.storage.browser.get('conversation_history', [])
    #             username = app.storage.user.get('username')
    #             if current_history and username:
    #                 user_db.create_conversation(
    #                     app.storage.browser['session_id'],
    #                     username,
    #                     str(current_history)
    #                 )
                
    #             # Create new session
    #             new_session_id = str(uuid.uuid4())
    #             print(f"New session created with ID: {new_session_id}")
                
    #             # Modify storage first
    #             app.storage.browser.update({
    #                 'session_id': new_session_id,
    #                 'conversation_history': []
    #             })
                
    #             # Create new conversation record only if we have a valid username
    #             if username:
    #                 user_db.create_conversation(
    #                     new_session_id,
    #                     username,
    #                     str([])
    #                 )
                
    #             # Navigate last
    #             ui.navigate.to('/chat')
            
    #         ui.button('New Session', on_click=new_session).props('flat color=primary')
    #         ui.label(f'Session ID: {app.storage.browser["session_id"]}').classes('text-xs')


    session_id = str(uuid.uuid4())
    app.storage.browser['session_id'] = session_id
    app.storage.browser['conversation_history'] = []



    # Main content
    with ui.column().classes('w-full max-w-2xl mx-auto p-4'):
        ui.label('Interactive Visit Planning Chat').classes('text-h4 q-mb-md')
        
        # Header with user info
        with ui.row().classes('w-full bg-gray-100 p-4 rounded-lg'):
            ui.label(f'User: {app.storage.user.get("username")}').classes('text-lg')
            ui.label(f'Session: {app.storage.browser["session_id"]}').classes('text-lg')
        
        # Chat display
        chat_display = ui.markdown('').classes('w-full h-64 border rounded-lg p-4 overflow-auto')
        
        # Message input
        message_input = ui.textarea('Type your message here...').classes('w-full h-64')
        
        def send_message():
            if not message_input.value:
                return
            
            # Add user message to history
            user_message = f'**User:** {message_input.value}'
            app.storage.browser['conversation_history'].append(user_message)
            
            # Update chat display
            chat_display.content = '\n\n'.join(app.storage.browser['conversation_history'])
            
            # Get response from LangFlow
            response = run_flow(message_input.value)
            
            # Add assistant message to history
            assistant_message = f'**Assistant:** {response["outputs"][0]["outputs"][0]["results"]["message"]["text"]}'
            app.storage.browser['conversation_history'].append(assistant_message)
            
            # Update chat display
            chat_display.content = '\n\n'.join(app.storage.browser['conversation_history'])
            
            # Clear input
            message_input.value = ''
            
            # Save conversation to database
            user_db.update_conversation(
                app.storage.browser['session_id'],
                str(app.storage.browser['conversation_history'])
            )
        
        # Send button
        ui.button('Send', on_click=send_message).classes('w-full')

        ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')

