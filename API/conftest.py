import pytest
import os
import json

CONFIG_PATH = 'C:\\Users\\MunFei_Woo\\python-webui-testing\\config\\config.json'


def pytest_addoption(parser):
    parser.addoption("--token", action="store", default="None")
    parser.addoption("--projecturl", action="store", default="None")
    parser.addoption("--projecttaskurl", action="store", default="None")


def pytest_configure(config):
    os.environ['token'] = config.getoption('token')
    os.environ['projecturl'] = config.getoption('projecturl')
    os.environ['projecttaskurl'] = config.getoption('projecttaskurl')


@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data


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


@pytest.fixture
def api_test_config(config_token, config_project_url, config_project_task_url, request):
    # Initialize WebDriver

    test_config = dict()
    test_config['token'] = config_token
    test_config['project_url'] = config_project_url
    test_config['project_task_url'] = config_project_task_url
    return test_config
