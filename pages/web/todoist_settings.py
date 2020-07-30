class TodoistSettings:

    SETTING_MENU_BTN = '//button[@aria-label="Setting"]'
    LOGOUT = '//div[text()="Log out"]'

    def __init__(self, browser):
        self.browser = browser

    def get_setting_menu(self):
        self.browser.find_element_by_xpath(self.SETTING_MENU_BTN).click()

    def select_logout(self):
        self.browser.find_element_by_xpath(self.LOGOUT).click()

