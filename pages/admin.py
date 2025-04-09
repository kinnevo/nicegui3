from nicegui import ui, app
from utils import initialize_users

@ui.page('/admin')
def admin_page():
    with ui.column().classes('w-full items-center'):
        ui.label('Welcome to SV Exploration Admin Page!').classes('text-h4 q-mb-md')

        with ui.column().classes('w-full items-center'):
            ui.label('List of Users').classes('text-h5 q-my-md text-center')

        # Create table reference
        table = None

        def refresh_table():
            nonlocal table
            if table:
                table.rows = list(app.storage.general.get('user_list', {}).values())
                table.update()

        def rebuild_users():
            app.storage.general['user_list'] = initialize_users()
            ui.notify('User list has been rebuilt')
            refresh_table()

        def reset_users():
            for user in app.storage.general['user_list'].values():
                user['logged'] = False
            ui.notify('All users have been reset')
            refresh_table()

        with ui.row().classes('w-full justify-center gap-4 q-mb-md'):
            ui.button('Rebuild User List', on_click=rebuild_users).classes('bg-green-500 text-white')
            ui.button('Reset All Users', on_click=reset_users).classes('bg-red-500 text-white')

        with ui.card().classes('w-full max-w-3xl mx-auto shadow-lg'):
            columns = [
                {'name': 'username', 'label': 'User Name', 'field': 'username'},
                {'name': 'timestamp', 'label': 'Date & Time', 'field': 'timestamp'},
                {'name': 'logged', 'label': 'Logged', 'field': 'logged'}
            ]
            
            # Store table reference
            table = ui.table(
                columns=columns,
                rows=list(app.storage.general.get('user_list', {}).values()),
            )

        # Add event listener for updates from other pages
        ui.add_body_html('''
            <script>
            window.addEventListener('admin-page-update', function() {
                window.location.reload();
            });
            </script>
        ''')

        ui.separator().classes('w-full q-my-md')
        ui.button('Return to Home', on_click=lambda: ui.navigate.to('/')).classes('bg-blue-500 text-white')
