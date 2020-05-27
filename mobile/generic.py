import time

from pages.mobile.todoist_leftNav import TodoistLeftNav
from pages.mobile.todoist_settings import TodoistSettings
from pages.mobile.todoist_about import TodoistAbout

class TodoistGeneric:

    def sync_data(app):
        left_nav = TodoistLeftNav(app)
        left_nav.get_main_menu()
        left_nav.select_settings()
        settings = TodoistSettings(app)
        settings.select_about_option()
        about = TodoistAbout(app)
        about.select_sync()
        time.sleep(5)
        about.select_navigate_up()
        time.sleep(2)
        settings.select_navigate_up()