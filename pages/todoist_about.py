class TodoistAbout:

    LAST_SYNC_OPTION = "//android.widget.TextView[@text='Last synced']"
    NAVIGATE_UP = "//android.widget.ImageButton[@content-desc='Navigate up']"

    def __init__(self,app):
        self.app = app

    def select_sync(self):
        self.app.find_element_by_xpath(self.LAST_SYNC_OPTION).click()

    def select_navigate_up(self):
        self.app.find_element_by_xpath(self.NAVIGATE_UP).click()

