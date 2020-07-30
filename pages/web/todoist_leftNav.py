class TodoistLeftNav:

    MAIN_MENU_BTN = '//button[@class="left_menu_toggle top_bar_btn"]'
    PROJECT_MAIN_MENU = '//button[text()="Projects"]'
    PROJECT_SELECTION = '//td/span[text() = "{}"]'

    def __init__(self, browser):
        self.browser = browser

    def get_main_menu(self):
        self.browser.find_element_by_xpath(self.MAIN_MENU_BTN).click()

    def select_project_option(self):
        self.browser.find_element_by_xpath(self.PROJECT_MAIN_MENU).click()

    def select_a_project_by_project_name(self, project_name):
        project = self.PROJECT_SELECTION.format(project_name)
        self.browser.find_element_by_xpath(project).click()

