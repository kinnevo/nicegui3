from nicegui import ui, app
import requests
import json
from datetime import datetime
import os
from typing import List, Optional
import uuid
from dotenv import load_dotenv
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

def find_user_from_pool():
    for username, user_data in app.storage.general['user_list'].items():
        if not user_data.get('logged', False):
            user_data['logged'] = True
            # Refresh admin page if it's open
            ui.run_javascript('window.dispatchEvent(new Event("admin-page-update"))')
            return username, username
    return -1, None


"""Add a message to the conversation history."""
def add_to_history(role: str, content: str, agent: str = "Unknown User", session_id: str = ""):
    message = {
        "role": role,
        "content": content,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agent": agent
    } 
    app.storage.browser['conversation_history'].append(message)

def display_conversation(conversation_history_txt, chat_display):
    # Build the complete content
    content = ""
    for message in conversation_history_txt:
        content += f'**{message["role"]}:** {message["content"]}\n\n'
    # Set the content once
    chat_display.content = content





@ui.page('/chat')
def chat_page():


    session_id = str(uuid.uuid4())
    app.storage.browser['session_id'] = session_id
    app.storage.browser['conversation_history'] = []

# get a user from the pool

    user_id, username = find_user_from_pool()
    app.storage.user['username'] = username

    if user_id == -1:    
        with ui.dialog() as error_dialog:
            with ui.card():
                ui.label(f'No users available at this time, try again later').classes('text-h6 q-mb-md')
                with ui.row().classes('w-full justify-end gap-2'):
                    ui.button('Go Back', on_click=lambda: ui.navigate.to('/')).classes('bg-gray-500 text-white')
        error_dialog.open()


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
            
            # Add user message and update display
            add_to_history(role='user', content=message_input.value, agent=app.storage.user.get("username", "Unknown User"), session_id=session_id)
            display_conversation(app.storage.browser['conversation_history'], chat_display)
            
            # Get and add assistant response
            response = run_flow(message_input.value)
            add_to_history(role='assistant', content=response["outputs"][0]["outputs"][0]["results"]["message"]["text"], agent=app.storage.user.get("username", "Unknown User"), session_id=session_id)
            display_conversation(app.storage.browser['conversation_history'], chat_display)
            
            # Clear input
            message_input.value = ''
            
            # Save conversation to database
            save_db()
        
            #print(app.storage.browser['conversation_history'])
            #print(f"Assistant: {app.storage.browser['conversation_history']}")

        # Send button
        ui.button('Send', on_click=send_message).classes('w-full')

        with ui.row().classes('w-full max-w-2xl mx-auto p-4'):

            ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
            ui.button('Cierra la sessión', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
            ui.button('Download a Files', on_click=download_file).classes('bg-blue-500 text-white')
            ui.button('Save DB', on_click=save_db).classes('bg-blue-500 text-white')

def download_file():
    import json
    from datetime import datetime
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"conversation_{app.storage.user.get('username', 'user')}_{timestamp}.json"
    
    # Convert conversation history to JSON string with proper encoding
    content = json.dumps(app.storage.browser['conversation_history'], 
                        ensure_ascii=False, 
                        indent=2)
    
    # Create download link
    ui.download(content.encode('utf-8'), filename)

def save_db():
    session_id = app.storage.browser['session_id']
    username = app.storage.user.get('username', 'Unknown User')
    conversation = str(app.storage.browser['conversation_history'])
    
    # Check if conversation exists
    existing_conversation = user_db.get_conversation(session_id)
    
    if existing_conversation:

        # Update existing conversation
        success = user_db.update_conversation(session_id, conversation)
        ui.notify('Conversation updated' if success else 'Update failed')
    else:

        # Create new conversation
        success = user_db.create_conversation(session_id, username, conversation)

        ui.notify('Conversation saved' if success else 'Save failed')
