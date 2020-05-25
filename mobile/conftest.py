import pytest
import os
import json

from appium import webdriver

CONFIG_PATH = 'config\\config.json'


def pytest_addoption(parser):
    parser.addoption("--appiumserver", action="store", default="None")
    parser.addoption("--platformname", action="store", default="None")
    parser.addoption("--platformversion", action="store", default="None")
    parser.addoption("--token", action="store", default="None")
    parser.addoption("--projecturl", action="store", default="None")
    parser.addoption("--projecttaskurl", action="store", default="None")
    parser.addoption("--email", action="store", default="None")
    parser.addoption("--password", action="store", default="None")


def pytest_configure(config):
    os.environ['appiumserver'] = config.getoption('appiumserver')
    os.environ['platformname'] = config.getoption('platformname')
    os.environ['platformversion'] = config.getoption('platformversion')
    os.environ['token'] = config.getoption('token')
    os.environ['projecturl'] = config.getoption('projecturl')
    os.environ['projecttaskurl'] = config.getoption('projecttaskurl')
    os.environ['email'] = config.getoption('email')
    os.environ['password'] = config.getoption('password')


@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture(scope='session')
def config_platform_name(configure):
    # Validate and return the browser choice from the config data

    platform = os.getenv('platformname')

    if platform != 'None':
        return platform
    else:
        if 'platform_name' not in configure:
            raise Exception('The config file does not contain "platform_name"')
        return configure['platform_name']


@pytest.fixture(scope='session')
def config_appium_server(configure):
    appium_server = os.getenv('appiumserver')

    if appium_server != 'None':
        return appium_server
    else:
        if 'appium_server' not in configure:
            raise Exception('The config file does not contain "appium_server"')
        return configure['appium_server']


@pytest.fixture(scope='session')
def config_platform_version(configure):
    platform_version = os.getenv('platform_version')

    if platform_version != 'None':
        return platform_version
    else:
        if 'platform_version' not in configure:
            raise Exception('The config file does not contain "platform_version"')
        return configure['platform_version']


@pytest.fixture(scope='session')
def config_token(configure):
    # Validate and return the browser choice from the config data

    token = os.getenv('token')

    if token != 'None':
        return token
    else:
        if 'token' not in configure:
            raise Exception('The config file does not contain "token"')
        return configure['token']


@pytest.fixture(scope='session')
def config_project_url(configure):
    project_url = os.getenv('projecturl')

    if project_url != 'None':
        return project_url
    else:
        if 'project_url' not in configure:
            raise Exception('The config file does not contain "project_url"')
        return configure['project_url']


@pytest.fixture(scope='session')
def config_project_task_url(configure):
    project_task_url = os.getenv('projecttaskurl')

    if project_task_url != 'None':
        return project_task_url
    else:
        if 'project_task_url' not in configure:
            raise Exception('The config file does not contain "project_task_url"')
        return configure['project_task_url']


@pytest.fixture(scope='session')
def config_email(configure):
    email = os.getenv('email')

    if email != 'None':
        return email
    else:
        if 'email' not in configure:
            raise Exception('The config file does not contain "email"')
        return configure['email']


@pytest.fixture(scope='session')
def config_password(configure):
    password = os.getenv('password')

    if password != 'None':
        return password
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
    test_config['token'] = config_token
    test_config['project_url'] = config_project_url
    test_config['project_task_url'] = config_project_task_url
    return test_config


@pytest.fixture
def app(config_platform_name, config_appium_server, config_platform_version, request):
    # Initialize WebDriver
    desired_caps = dict()
    desired_caps['platformName'] = config_platform_name
    desired_caps['platformVersion'] = config_platform_version
    desired_caps['appPackage'] = 'com.todoist'
    desired_caps['appActivity'] = 'com.todoist.activity.HomeActivity'
    desired_caps['noRest'] = 'True'

    driver = webdriver.Remote(config_appium_server, desired_capabilities=desired_caps)

    driver.implicitly_wait(10)

    # Return the driver object at the end of setup
    yield driver

    # For cleanup, quit the driver
    driver.quit()