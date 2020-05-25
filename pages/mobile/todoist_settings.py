from appium.webdriver.common.touch_action import TouchAction

class TodoistSettings:

    ABOUT_OPTION = '//android.widget.TextView[@text="About"]'
    GENERAL_OPTION = '//android.widget.TextView[@text="General"]'
    SUPPORT_OPTION = '//android.widget.TextView[@text="Support"]'
    NAVIGATE_UP = "//android.widget.ImageButton[@content-desc='Navigate up']"

    def __init__(self, app):
        self.app = app

    def select_about_option(self):
        element_to_press = self.app.find_element_by_xpath(self.SUPPORT_OPTION)
        element_to_move = self.app.find_element_by_xpath(self.GENERAL_OPTION)
        actions = TouchAction(self.app)
        actions.press(element_to_press)
        actions.move_to(element_to_move)
        actions.perform()
        self.app.find_element_by_xpath(self.ABOUT_OPTION).click()

    def select_navigate_up(self):
        self.app.find_element_by_xpath(self.NAVIGATE_UP).click()



