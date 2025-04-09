from nicegui import ui, app
from datetime import datetime
import secrets
import random
import langflow_chat


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
            
        
        with ui.tab_panels(tabs, value=section1).classes('w-full'):

            with ui.tab_panel(section1):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 1').classes('text-h4 q-mb-md')
                    ui.separator().classes('w-full q-my-md')
                     
                    ui.separator().classes('w-full q-my-md')
                    ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    

                    
            with ui.tab_panel(section2):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 2').classes('text-h4 q-mb-md')
                    ui.separator().classes('w-full q-my-md')
                    ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    
            with ui.tab_panel(section3):
                with ui.column().classes('w-full items-center'):
                    ui.label('Section 3').classes('text-h4 q-mb-md')
                    
                    ui.separator().classes('w-full q-my-md')
                    ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
                    
