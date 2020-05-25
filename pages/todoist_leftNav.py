class TodoistLeftNav:

    MAIN_MENU_BTN = '//android.widget.ImageButton[@content-desc="Change the current view"]'
    PROJECT_MAIN_MENU = '//android.widget.TextView[@text="Projects"]'
    PROJECT_MANAGE_OPTION = '//android.widget.TextView[@text="Manage projects"]'
    SETTINGS_MAIN_MENU = '//android.widget.TextView[@text="Settings"]'

    def __init__(self, app):
        self.app = app

    def get_main_menu(self):
        self.app.find_element_by_xpath(self.MAIN_MENU_BTN).click()

    def select_project_option(self):
        self.app.find_element_by_xpath(self.PROJECT_MAIN_MENU).click()

    def select_manage_project_option(self):
        self.app.find_element_by_xpath(self.PROJECT_MANAGE_OPTION).click()

    def select_a_project_by_project_name(self, project_name):
        project = "//android.widget.TextView[@text = '{}']".format(project_name)
        self.app.find_element_by_xpath(project).click()

    def select_settings(self):
        self.app.find_element_by_xpath(self.SETTINGS_MAIN_MENU).click()
