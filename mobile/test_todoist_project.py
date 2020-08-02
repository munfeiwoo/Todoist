import pytest
import time
import logging

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id
from pages.mobile.todoist_leftNav import TodoistLeftNav
from pages.mobile.todoist_login import TodoistLogin
from pages.mobile.todoist_manage_project import TodoistManageProject


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.Mobile
def test_create_project(app, api, user):

    # Setup
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'test_create_project'
    token = api['api_token']
    project_url = api['api_project_url']
    email = user['email']
    password = user['password']

    api_remove_projects_by_project_name(token, project_url, project_name)

    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'

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
    api_remove_project_by_project_id(token, project_url, project_id)
