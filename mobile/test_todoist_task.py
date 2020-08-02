import pytest
import time
import logging

from api.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details, \
    api_get_project_id_by_project_name, api_remove_projects_by_project_name, api_remove_project_by_project_id
from api.test_todoist_task import api_get_project_task_by_name, api_get_project_task_id_by_name, api_reopen_task
from pages.mobile.todoist_login import TodoistLogin
from pages.mobile.todoist_leftNav import TodoistLeftNav
from pages.mobile.todoist_project import TodoistProject
from mobile.generic import sync_data


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_task_creation(app, api, user):
    # Setup
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'test_task_creation'
    task_title = 'testing 123'
    task_datetime = '26 June 2020 11am'
    token = api['api_token']
    project_url = api['api_project_url']
    project_task_url = api['api_project_task_url']
    email = user['email']
    password = user['password']

    api_remove_projects_by_project_name(token, project_url, project_name)

    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'

    # Body
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(3)

    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_a_project_by_project_name(project_name)

    project_page = TodoistProject(app)
    project_page.select_add_task()
    project_page.add_task_title(task_title)
    project_page.submit_task_schedule(task_datetime)
    project_page.submit_schedule()
    project_page.submit_task()
    time.sleep(5)

    assert api_get_project_task_by_name(token, project_task_url, project_id, task_title) is not None, \
        'Task Title should not be None'

    # Teardown
    api_remove_project_by_project_id(token, project_url, project_id)


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_reopen_task(app, api, user):
    # Setup
    # project name used for each automated test must be unique to ensure each test is standalone
    project_name = 'reopen_task'
    task_title = 'testing 1234'
    task_datetime = '26 June 2020 11am'
    token = api['api_token']
    project_url = api['api_project_url']
    project_task_url = api['api_project_task_url']
    email = user['email']
    password = user['password']

    api_remove_projects_by_project_name(token, project_url, project_name)

    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'

    # Body
    login = TodoistLogin(app)
    login.email_login(email, password)
    time.sleep(3)

    left_nav = TodoistLeftNav(app)
    left_nav.get_main_menu()
    left_nav.select_project_option()
    left_nav.select_a_project_by_project_name(project_name)

    project_page = TodoistProject(app)
    project_page.select_add_task()
    project_page.add_task_title(task_title)
    project_page.submit_task_schedule(task_datetime)
    project_page.submit_schedule()
    project_page.submit_task()
    time.sleep(5)

    task_id = api_get_project_task_id_by_name(token, project_task_url, project_id, task_title)
    assert task_id is not None, 'Task id should not be None'
    app.back()

    time.sleep(5)
    left_nav.get_main_menu()
    time.sleep(3)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)

    project_page.mark_completed_project_task_by_name(task_title)
    time.sleep(5)

    api_reopen_task(token, project_task_url, task_id)

    sync_data(app)

    time.sleep(5)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)
    assert project_page.get_project_task_by_name(task_title) is not None, \
        'Should be able to find task "{}" in the project'.format(task_title)

    # Teardown
    api_remove_project_by_project_id(token, project_url, project_id)
