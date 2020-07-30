from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.common.exceptions import NoSuchElementException


class TodoistLogin:
    URL = 'https://todoist.com/users/showlogin'
    EMAIL_INPUT = '//input[@type="email" and @name="email"]'
    PASSWORD_INPUT = '//input[@type="password" and @name="password"]'
    LOGIN_BTN = '//button[text()="Log in"]'
    LOGIN_FAILED_ERROR = '//span[text()="Wrong email or password."]'

    def __init__(self, browser):
        self.browser = browser

    def load(self):

        self.browser.get(self.URL)

    def email_login(self, email, password):
        self.browser.find_element_by_xpath(self.EMAIL_INPUT).send_keys(email)
        self.browser.find_element_by_xpath(self.PASSWORD_INPUT).send_keys(password)
        self.browser.find_element_by_xpath(self.LOGIN_BTN).click()

    def check_if_login_successful(self):
        try:
            results = self.browser.find_element_by_xpath(self.LOGIN_FAILED_ERROR)
            if results is not None:
                return "failed"
        except NoSuchElementException:
            return "successful"
