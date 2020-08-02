import pytest
import os
import json

from util.fileaccess import load_json_file
from util.es import es_connect

CONFIG_PATH = 'config\\config.json'


# Getting values from command line
def pytest_addoption(parser):
    parser.addoption("--es_server", action="store", default="None")
    parser.addoption("--es_port", action="store", default="None")
    parser.addoption("--es_username", action="store", default="None")
    parser.addoption("--es_password", action="store", default="None")


# Setting values from command line to global variables
def pytest_configure(config):
    global ES_SERVER
    global ES_PORT
    global ES_USERNAME
    global ES_PASSWORD

    ES_SERVER = config.getoption('es_server')
    ES_PORT = config.getoption('es_port')
    ES_USERNAME = config.getoption('es_username')
    ES_PASSWORD = config.getoption('es_password')


# Load configuration from config file
@pytest.fixture(scope='session')
def configure():
    # Read the JSON config file and returns it as a parsed dict
    return load_json_file(CONFIG_PATH)


# Configure Elasticsearch server name
@pytest.fixture(scope='session')
def config_es_server(configure):
    if ES_SERVER != 'None':
        return ES_SERVER
    else:
        if 'es_server' not in configure:
            raise Exception('The config file does not contain "es_server"')
        return configure['es_server']


# Configure Elasticsearch server port
@pytest.fixture(scope='session')
def config_es_port(configure):
    if ES_PORT != 'None':
        return ES_PORT
    else:
        if 'es_port' not in configure:
            raise Exception('The config file does not contain "es_port"')
        return configure['es_port']


# Configure Elasticsearch server username
@pytest.fixture(scope='session')
def config_es_username(configure):
    if ES_USERNAME != 'None':
        return ES_USERNAME
    else:
        if 'es_username' not in configure:
            raise Exception('The config file does not contain "es_username"')
        return configure['es_username']


# Configure Elasticsearch server password
@pytest.fixture(scope='session')
def config_es_password(configure):
    if ES_PASSWORD != 'None':
        return ES_PASSWORD
    else:
        if 'es_password' not in configure:
            raise Exception('The config file does not contain "es_password"')
        return configure['es_password']


# Configure and return Elasticsearch server connection
@pytest.fixture
def es(config_es_server, config_es_port, config_es_username, config_es_password, request):
    # Initialize WebDriver

    es_server = es_connect(config_es_server, config_es_port, config_es_username, config_es_password)

    # Return the driver object at the end of setup
    yield es_server

    # For cleanup, quit the driver
    es_server.close()
