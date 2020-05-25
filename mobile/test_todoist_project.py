import pytest
import time

from API.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details
from pages.todoist_leftNav import TodoistLeftNav
from pages.todoist_login import TodoistLogin
from pages.todoist_manage_project import TodoistManageProject


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.Mobile
def test_create_project(app, api, user):

    # Setup
    project_name = 'Setel Project1'
    token = api['token']
    project_url = api['project_url']
    email = user['email']
    password = user['password']
    project_id = api_create_new_project(token, project_url, project_name)
    assert (project_id > 0)

    # Body
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(5)

    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_manage_project_option()
    time.sleep(5)

    manage_project = TodoistManageProject(app)
    manage_project.check_project_exist_by_project_name(project_name)

    # Teardown
    api_delete_project(token, project_url, project_id)
    response = api_get_project_details(token, project_url, project_id)
    assert (response.status_code == 404)