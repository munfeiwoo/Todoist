import pytest
import os
import json

from selenium.webdriver import Chrome, Firefox, Ie
from util.fileaccess import load_json_file

CONFIG_PATH = 'config\\config.json'
TOKEN = ''
PROJECT_URL = ''
PROJECT_TASK_URL = ''
EMAIL = ''
PASSWORD = ''
TEST_BROWSER = ''
DEFAULT_WAIT_TIME = 10
SUPPORTED_BROWSERS = ['chrome', 'firefox', 'Ie']


def pytest_addoption(parser):
    parser.addoption("--token", action="store", default="None")
    parser.addoption("--projecturl", action="store", default="None")
    parser.addoption("--projecttaskurl", action="store", default="None")
    parser.addoption("--email", action="store", default="None")
    parser.addoption("--password", action="store", default="None")
    parser.addoption("--testbrowser", action="store", default="None")


def pytest_configure(config):
    global TOKEN
    global PROJECT_URL
    global PROJECT_TASK_URL
    global EMAIL
    global PASSWORD
    global TEST_BROWSER

    TOKEN = config.getoption('token')
    PROJECT_URL = config.getoption('projecturl')
    PROJECT_TASK_URL = config.getoption('projecttaskurl')
    EMAIL = config.getoption('email')
    PASSWORD = config.getoption('password')
    TEST_BROWSER = config.getoption('testbrowser')


@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict

    return load_json_file(CONFIG_PATH)


@pytest.fixture(scope='session')
def config_token(configure):
    if TOKEN != 'None':
        return TOKEN
    else:
        if 'api_token' not in configure:
            raise Exception('The config file does not contain "token"')
        return configure['api_token']


@pytest.fixture(scope='session')
def config_project_url(configure):
    if PROJECT_URL != 'None':
        return PROJECT_URL
    else:
        if 'api_project_url' not in configure:
            raise Exception('The config file does not contain "project_url"')
        return configure['api_project_url']


@pytest.fixture(scope='session')
def config_project_task_url(configure):
    if PROJECT_TASK_URL != 'None':
        return PROJECT_TASK_URL
    else:
        if 'api_project_task_url' not in configure:
            raise Exception('The config file does not contain "project_task_url"')
        return configure['api_project_task_url']


@pytest.fixture(scope='session')
def config_email(configure):
    if EMAIL != 'None':
        return EMAIL
    else:
        if 'email' not in configure:
            raise Exception('The config file does not contain "email"')
        return configure['email']


@pytest.fixture(scope='session')
def config_password(configure):
    if PASSWORD != 'None':
        return PASSWORD
    else:
        if 'password' not in configure:
            raise Exception('The config file does not contain "password"')
        return configure['password']


@pytest.fixture(scope='session')
def config_browser(configure):
    # Validate and return the browser choice from the config data

    if TEST_BROWSER != 'None':
        if TEST_BROWSER not in SUPPORTED_BROWSERS:
            raise Exception(TEST_BROWSER + ' is not a supported browser')
        else:
            return TEST_BROWSER
    else:
        if 'browser' not in configure:
            raise Exception('The config file does not contain "browser"')
        elif configure['browser'] not in SUPPORTED_BROWSERS:
            raise Exception(f'"{configure["browser"]}" is not a supported browser')
        return configure['browser']


@pytest.fixture(scope='session')
def config_wait_time(configure):
    # Validate and return the wait time from the config data
    return configure['wait_time'] if 'wait_time' in configure else DEFAULT_WAIT_TIME


@pytest.fixture
def user(config_email, config_password, request):
    user_config = dict()
    user_config['email'] = config_email
    user_config['password'] = config_password
    return user_config


@pytest.fixture
def api(config_token, config_project_url, config_project_task_url, request):
    # Initialize WebDriver

    test_config = dict()
    test_config['api_token'] = config_token
    test_config['api_project_url'] = config_project_url
    test_config['api_project_task_url'] = config_project_task_url
    return test_config


@pytest.fixture
def browser(config_browser, config_wait_time, request):
    # Initialize WebDriver
    if config_browser == 'chrome':
        driver = Chrome()
    elif config_browser == 'firefox':
        driver = Firefox()
    elif config_browser == 'Ie':
        driver = Ie()
    else:
        raise Exception(f'"{config_browser}" is not a supported browser')

    # Wait implicitly for elements to be ready before attempting interactions
    driver.implicitly_wait(config_wait_time)
    driver.maximize_window()
    failed_before = request.session.testsfailed

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()
