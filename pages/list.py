from nicegui import ui, app
from datetime import datetime
import secrets
import random
import langflow_chat

# Sample data - in a real app you would fetch this from your database
users = [
    {"name": "John Doe", "timestamp": datetime(2025, 4, 5, 14, 30)},
    {"name": "Jane Smith", "timestamp": datetime(2025, 4, 6, 9, 15)},
    {"name": "Robert Johnson", "timestamp": datetime(2025, 4, 6, 10, 45)},
    {"name": "Emily Williams", "timestamp": datetime(2025, 4, 5, 16, 20)},
    {"name": "Michael Brown", "timestamp": datetime(2025, 4, 4, 11, 5)}
]


def list_page():
    with ui.column().classes('w-full items-center'):
        ui.label('User Management').classes('text-h3 q-mb-md')
        
        # Status line
        def update_status():
            count = len(app.storage.general.get('user_list', {}))
            status_label.set_text(f'Registered users: {count}')
        
        status_label = ui.label('Registered users: 0').classes('text-h5 q-mb-md')
        
        ui.link('Share Your Dreams', '/chat').props('flat color=primary')



        with ui.tabs().classes('w-full') as tabs:
            section1 = ui.tab('Section 1')
            section2 = ui.tab('Section 2')
            section3 = ui.tab('Section 3')
            
        # Move refresh_table outside the tab panel so it's accessible
        def refresh_table():
            table_content.clear()
            users = app.storage.general.get('user_list', {})
            for username, timestamp in users.items():
                with table_content:
                    with ui.row().classes('w-full border-b p-2'):
                        ui.label(username).classes('w-1/2')
                        ui.label(timestamp).classes('w-1/2')

        with ui.tab_panels(tabs, value=section1).classes('w-full'):
            with ui.tab_panel(section1):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 1').classes('text-h4 q-mb-md')
                    ui.separator().classes('w-full q-my-md')
                    
                    # User management row
                    with ui.row().classes('w-full items-center justify-center gap-4'):
                        # Editable username field
                        username = ui.input(label='Username', value=f'user_{secrets.token_hex(4)}').classes('w-1/4')
                        
                        # Date field
                        date_field = ui.input(label='Date', value=datetime.now().strftime('%Y-%m-%d %H:%M:%S')).classes('w-1/4')
                        
                        # Add button
                        ui.button('Add User', on_click=lambda: add_user()).classes('bg-green-500 text-white')
                        
                        # Remove button
                        def show_remove_dialog():
                            with ui.dialog() as dialog:
                                with ui.card():
                                    ui.label(f'Are you sure you want to remove user {username.value}?').classes('text-h6 q-mb-md')
                                    with ui.row().classes('w-full justify-end gap-2'):
                                        ui.button('Cancel', on_click=dialog.close).classes('bg-gray-500 text-white')
                                        ui.button('Confirm', on_click=lambda: (remove_user(username.value), dialog.close())).classes('bg-red-500 text-white')
                            dialog.open()

                        # Error message button
                        def show_error_dialog():
                            with ui.dialog() as error_dialog:
                                with ui.card():
                                    ui.label(f'Error message').classes('text-h6 q-mb-md')
                                    with ui.row().classes('w-full justify-end gap-2'):
                                        ui.button('Cancel', on_click=error_dialog.close).classes('bg-gray-500 text-white')
                            error_dialog.open()



                        ui.button('Remove User', on_click=show_remove_dialog).classes('bg-red-500 text-white')
                        
                        # Clear button
                        def clear_users():
                            app.storage.general['user_list'] = {}
                            update_status()
                            refresh_table()
                            
                        ui.button('Clear', on_click=clear_users).classes('bg-gray-500 text-white')
                    
                    ui.separator().classes('w-full q-my-md')
                    ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    
                    # Add table display below Return Home button
                    ui.separator().classes('w-full q-my-md')
                    
                    # Simple table header
                    with ui.row().classes('w-3/4 bg-blue-500 text-white p-2'):
                        ui.label('Username').classes('w-1/2 font-bold')
                        ui.label('Date and Time').classes('w-1/2 font-bold')
                    
                    # Simple table content
                    table_content = ui.column().classes('w-3/4')
                    refresh_table()  # Initial display
                    
            with ui.tab_panel(section2):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 2').classes('text-h4 q-mb-md')
                    ui.separator().classes('w-full q-my-md')
                    ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    
            with ui.tab_panel(section3):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 3').classes('text-h4 q-mb-md')


                with ui.card().classes('w-full max-w-3xl mx-auto shadow-lg'):

                    
                    # Create a title for the table
                    ui.label('List of Users').classes('text-h5 q-my-md text-center')
                    
                    # Create a basic table with minimal configuration
                    columns = [
                        {'name': 'name', 'label': 'User Name', 'field': 'name'},
                        {'name': 'timestamp', 'label': 'Date & Time', 'field': 'timestamp'}
                    ]
                    
                    # Basic table without any custom styling
                    ui.table(
                        columns=columns,
                        rows=users,
                    )

                    
                ui.separator().classes('w-full q-my-md')
                ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    
        def add_user():
            if not app.storage.general.get('user_list'):
                app.storage.general['user_list'] = {}
            
            # Generate a new random username
            new_username = f'user_{secrets.token_hex(4)}'
            # Get current timestamp
            current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Add the new user to the list
            app.storage.general['user_list'][new_username] = current_time
            
            update_status()
            refresh_table()
            
        def remove_user(username):
            if hasattr(app.storage.general, 'user_list') and username in app.storage.general['user_list']:
                del app.storage.general['user_list'][username]
                update_status()
                refresh_table()
