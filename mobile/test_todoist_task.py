import pytest
import time
import logging

from API.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id
from API.test_todoist_task import api_get_project_task_by_name, api_get_project_task_id_by_name, api_reopen_task
from pages.mobile.todoist_login import TodoistLogin
from pages.mobile.todoist_leftNav import TodoistLeftNav
from pages.mobile.todoist_project import TodoistProject
from mobile.generic import sync_data

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_task_creation(app, api, user):
    # Setup
    log.info('Setting up test environment to create_project')
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'test_task_creation'
    task_title = 'testing 123'
    task_datetime = '26 June 2020 11am'
    token = api['api_token']
    project_url = api['api_project_url']
    project_task_url = api['api_project_task_url']
    email = user['email']
    password = user['password']

    log.info('API CALL: Clean up project data')
    api_remove_projects_by_project_name(token, project_url, project_name)
    log.info('Project removed successfully during setup')

    log.info('API CALL: Create project using API')
    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'
    log.info("API CALL: Project created successfully")

    # Body
    log.info('Perform login')
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(3)
    log.info('Login successfully')

    log.info('Goto Left Nav and select a project')
    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_a_project_by_project_name(project_name)
    log.info('Project selected')

    log.info('Add task for a project')
    project_page = TodoistProject(app)
    project_page.select_add_task()
    project_page.add_task_title(task_title)
    project_page.submit_task_schedule(task_datetime)
    project_page.submit_schedule()
    project_page.submit_task()
    log.info('Task created for the project')
    time.sleep(5)

    log.info('API CALL: Verify task created using API')
    assert api_get_project_task_by_name(token, project_task_url, project_id, task_title) is not None, \
        'Task Title should not be None'
    log.info('API CALL: Task exist from API verification')

    # Teardown
    log.info('Remove and clean up project')
    api_remove_project_by_project_id(token, project_url, project_id)
    log.info('Project removed successfully')


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_reopen_task(app, api, user):
    # Setup
    log.info('Setting up test environment to create project')
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'reopen_task'
    task_title = 'testing 1234'
    task_datetime = '26 June 2020 11am'
    token = api['api_token']
    project_url = api['api_project_url']
    project_task_url = api['api_project_task_url']
    email = user['email']
    password = user['password']

    log.info('API CALL: Clean up project data')
    api_remove_projects_by_project_name(token, project_url, project_name)
    log.info('Project removed successfully during setup')

    log.info('API CALL: Create project using API')
    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'
    log.info('API CALL: Project created successfully')

    # Body
    log.info('Perform login')
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(3)
    log.info('Login successfully')

    log.info('Goto Left Nav and select project({})'.format(project_name))
    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_a_project_by_project_name(project_name)
    log.info('Project ({}) selected'.format(project_name))

    log.info('Add task to project ({})'.format(project_name))
    project_page = TodoistProject(app)
    project_page.select_add_task()
    project_page.add_task_title(task_title)
    project_page.submit_task_schedule(task_datetime)
    project_page.submit_schedule()
    project_page.submit_task()
    time.sleep(5)
    log.info('Task created to project ({})'.format(project_name))

    log.info('API CALL: Get task id by task title')
    task_id = api_get_project_task_id_by_name(token, project_task_url, project_id, task_title)
    assert task_id is not None, 'Task id should not be None'
    log.info('API CALL: Task id returned successfully')
    app.back()

    log.info('Navigate again to the project')
    time.sleep(5)
    left_nav.get_main_menu()
    time.sleep(3)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)
    log.info('Navigated successfully')

    log.info('Mark task to complete')
    project_page.mark_completed_project_task_by_name(task_title)
    time.sleep(5)
    log.info('Task marked to complete successfully')

    log.info('API CALL: Reopen Task')
    api_reopen_task(token, project_task_url, task_id)
    log.info('API CALL completed')

    log.info('Perform data sync in Mobile')
    sync_data(app)
    log.info('Data sync completed')

    log.info('Navigate back to project')
    time.sleep(5)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)
    assert project_page.get_project_task_by_name(task_title) is not None, \
        'Should be able to find task "{}" in the project'.format(task_title)
    log.info('Task has been reopened successfully and displaying')

    # Teardown

    log.info('Remove and clean up project')
    api_remove_project_by_project_id(token, project_url, project_id)
    log.info('Project removed successfully')
