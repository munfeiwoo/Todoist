class TodoistLogin:

    EMAIL_LOGIN_BTN = 'com.todoist:id/btn_welcome_email'
    ANDROID_CANCEL_BTN = 'com.google.android.gms:id/cancel'
    EMAIL_INPUT = 'com.todoist:id/email_exists_input'
    EMAIL_CONTINUE_BTN = 'com.todoist:id/btn_continue_with_email'
    PASSWORD_INPUT = 'com.todoist:id/log_in_password'
    LOGIN_BTN = 'com.todoist:id/btn_log_in'
    TIMEZONE_NO_SETUP_OPTION = 'android:id/button2'

    def __init__(self, app):
        self.app = app

    def email_login(self):
        self.app.find_element_by_id(self.EMAIL_LOGIN_BTN).click()
        self.app.find_element_by_id(self.ANDROID_CANCEL_BTN).click()
        self.app.find_element_by_id(self.EMAIL_INPUT).send_keys('munfei.woo@gmail.com')
        self.app.find_element_by_id(self.EMAIL_CONTINUE_BTN).click()
        self.app.find_element_by_id(self.PASSWORD_INPUT).send_keys("mel98223")
        self.app.find_element_by_id(self.LOGIN_BTN).click()
        self.app.find_element_by_id(self.TIMEZONE_NO_SETUP_OPTION).click()
