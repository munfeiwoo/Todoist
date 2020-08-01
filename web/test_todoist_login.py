import pytest
import time
import logging
import allure

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id

from pages.web.todoist_login import TodoistLogin
from pages.web.todoist_leftNav import TodoistLeftNav
from pages.web.todoist_project import TodoistProject

from util.fileaccess import load_csv_to_dict

LOGIN_TEST_DATA_PATH = 'data\\web\\login.csv'

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


def get_login_test_data():
    # Retrieve values from CSV
    login_test_data = load_csv_to_dict(LOGIN_TEST_DATA_PATH)
    return login_test_data


@pytest.mark.P1
@pytest.mark.Login
@pytest.mark.Web
@pytest.mark.parametrize(
    "data", get_login_test_data())
@allure.epic("Web")
@allure.feature("Feature - Login")
@allure.story("Story - User Login")
@allure.testcase("Test Case  - User login as expected")
def test_login(browser, data):

    login = TodoistLogin(browser)
    login.load()
    login.email_login(data["email"], data["password"])

    assert login.check_if_login_successful() == data["expected"]