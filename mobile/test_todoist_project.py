import pytest
import time
import logging

from API.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details
from pages.todoist_leftNav import TodoistLeftNav
from pages.todoist_login import TodoistLogin
from pages.todoist_manage_project import TodoistManageProject

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.Mobile
def test_create_project(app, api, user):

    # Setup
    log.info('Setting up test environment for test_create_project')
    project_name = 'Setel Project1'
    token = api['token']
    project_url = api['project_url']
    email = user['email']
    password = user['password']
    log.info('Create project using API')
    project_id = api_create_new_project(token, project_url, project_name)
    assert (project_id > 0)
    log.info('Project created successfully')

    # Body
    log.info('Perform login')
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(5)
    log.info('Login successfully')

    log.info('Goto Manage Project')
    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_manage_project_option()
    time.sleep(5)
    log.info('Manage Project loaded successfully')

    manage_project = TodoistManageProject(app)
    log.info('Check if project name exist')
    manage_project.check_project_exist_by_project_name(project_name)
    log.info('Project name exist in Manage Project page')

    # Teardown
    log.info('Remove and clean up project')
    api_delete_project(token, project_url, project_id)
    response = api_get_project_details(token, project_url, project_id)
    assert (response.status_code == 404)
    log.info('Project removed successfully')
