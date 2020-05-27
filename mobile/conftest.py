import pytest
import os
import json

from appium import webdriver
from util.fileaccess import load_json_file

CONFIG_PATH = 'config\\config.json'
UDID = ''
APPIUM_SERVER = ''
PLATFORM_NAME = ''
PLATFORM_VERSION = ''
TOKEN = ''
PROJECT_URL = ''
PROJECT_TASK_URL = ''
EMAIL = ''
PASSWORD = ''


def pytest_addoption(parser):
    parser.addoption("--appiumserver", action="store", default="None")
    parser.addoption("--platformname", action="store", default="None")
    parser.addoption("--platformversion", action="store", default="None")
    parser.addoption("--udid", action="store", default="None")
    parser.addoption("--token", action="store", default="None")
    parser.addoption("--projecturl", action="store", default="None")
    parser.addoption("--projecttaskurl", action="store", default="None")
    parser.addoption("--email", action="store", default="None")
    parser.addoption("--password", action="store", default="None")


def pytest_configure(config):
    global UDID
    global APPIUM_SERVER
    global PLATFORM_NAME
    global PLATFORM_VERSION
    global TOKEN
    global PROJECT_URL
    global PROJECT_TASK_URL
    global EMAIL
    global PASSWORD

    APPIUM_SERVER = config.getoption('appiumserver')
    PLATFORM_NAME = config.getoption('platformname')
    PLATFORM_VERSION = config.getoption('platformversion')
    TOKEN = config.getoption('token')
    PROJECT_URL = config.getoption('projecturl')
    PROJECT_TASK_URL = config.getoption('projecttaskurl')
    EMAIL = config.getoption('email')
    PASSWORD = config.getoption('password')
    UDID = config.getoption('udid')

@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict

    return load_json_file(CONFIG_PATH)


@pytest.fixture(scope='session')
def config_platform_name(configure):
    # Validate and return the browser choice from the config data

    if PLATFORM_NAME != 'None':
        return PLATFORM_NAME
    else:
        if 'platform_name' not in configure:
            raise Exception('The config file does not contain "platform_name"')
        return configure['platform_name']


@pytest.fixture(scope='session')
def config_appium_server(configure):

    if APPIUM_SERVER != 'None':
        return APPIUM_SERVER
    else:
        if 'appium_server' not in configure:
            raise Exception('The config file does not contain "appium_server"')
        return configure['appium_server']


@pytest.fixture(scope='session')
def config_platform_version(configure):

    if PLATFORM_VERSION != 'None':
        return PLATFORM_VERSION
    else:
        if 'platform_version' not in configure:
            raise Exception('The config file does not contain "platform_version"')
        return configure['platform_version']


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
def app(config_platform_name, config_appium_server, config_platform_version, request):
    # Initialize WebDriver
    desired_caps = dict()
    desired_caps['platformName'] = config_platform_name
    desired_caps['platformVersion'] = config_platform_version
    if UDID != 'None':
        desired_caps['udid'] = UDID
    desired_caps['appPackage'] = 'com.todoist'
    desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'
    desired_caps['noRest'] = 'True'

    driver = webdriver.Remote(config_appium_server, desired_capabilities=desired_caps)

    driver.implicitly_wait(10)

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()