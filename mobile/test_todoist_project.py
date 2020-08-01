import pytest
import time
import logging

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id
from pages.mobile.todoist_leftNav import TodoistLeftNav
from pages.mobile.todoist_login import TodoistLogin
from pages.mobile.todoist_manage_project import TodoistManageProject

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.Mobile
def test_create_project(app, api, user):

    # Setup
    log.info('Setting up test environment for test_create_project')
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'test_create_project'
    token = api['api_token']
    project_url = api['api_project_url']
    email = user['email']
    password = user['password']

    log.info('api CALL: Clean up project data')
    api_remove_projects_by_project_name(token, project_url, project_name)
    log.info('Project removed successfully during setup')

    log.info('api CALL: Create project using api')
    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'
    log.info('api CALL: Project created successfully')

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
    api_remove_project_by_project_id(token, project_url, project_id)
    log.info('Project removed successfully')