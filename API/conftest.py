import pytest
import os
import json

CONFIG_PATH = 'config\\config.json'
API_TOKEN = ''
API_PROJECT_URL = ''
API_PROJECT_TASK_URL = ''


def pytest_addoption(parser):
    parser.addoption("--apitoken", action="store", default="None")
    parser.addoption("--apiprojecturl", action="store", default="None")
    parser.addoption("--apiprojecttaskurl", action="store", default="None")


def pytest_configure(config):
    global API_TOKEN
    global API_PROJECT_URL
    global API_PROJECT_TASK_URL

    API_TOKEN = config.getoption('apitoken')
    API_PROJECT_URL = config.getoption('apiprojecturl')
    API_PROJECT_TASK_URL = config.getoption('apiprojecttaskurl')


@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict
    with open(CONFIG_PATH) as config_file:
        data = json.load(config_file)
    return data


@pytest.fixture(scope='session')
def config_token(configure):
    # Validate and return the browser choice from the config data

    if API_TOKEN != 'None':
        return API_TOKEN
    else:
        if 'api_token' not in configure:
            raise Exception('The config file does not contain "token"')
        return configure['api_token']


@pytest.fixture(scope='session')
def config_project_url(configure):

    if API_PROJECT_URL != 'None':
        return API_PROJECT_URL
    else:
        if 'api_project_url' not in configure:
            raise Exception('The config file does not contain "project_url"')
        return configure['api_project_url']


@pytest.fixture(scope='session')
def config_project_task_url(configure):

    if API_PROJECT_TASK_URL != 'None':
        return API_PROJECT_TASK_URL
    else:
        if 'api_project_task_url' not in configure:
            raise Exception('The config file does not contain "project_task_url"')
        return configure['api_project_task_url']


@pytest.fixture
def api_test_config(config_token, config_project_url, config_project_task_url, request):
    # Initialize WebDriver

    config = dict()
    config['api_token'] = config_token
    config['api_project_url'] = config_project_url
    config['api_project_task_url'] = config_project_task_url
    return config