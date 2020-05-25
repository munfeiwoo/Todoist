import pytest
import time

from API.test_todoist_project import api_create_new_project, api_delete_project, api_get_project_details
from API.test_todoist_task import api_get_project_task_by_name, api_get_project_task_id_by_name, api_reopen_task
from pages.todoist_login import TodoistLogin
from pages.todoist_leftNav import TodoistLeftNav
from pages.todoist_project import TodoistProject
from mobile.generic import TodoistGeneric


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_task_creation(app, api, user):

    # Setup
    project_name = 'Setel Project2'
    task_title = 'testing 123'
    task_datetime = '26 June 2020 11am'
    token = api['token']
    project_url = api['project_url']
    project_task_url = api['project_task_url']
    email = user['email']
    password = user['password']
    project_id = api_create_new_project(token, project_url,project_name)
    assert (project_id > 0)

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
    assert (api_get_project_task_by_name(token, project_task_url, project_id, task_title) is not None)

    # Teardown
    api_delete_project(token, project_url, project_id)
    response = api_get_project_details(token, project_url,project_id)
    assert (response.status_code == 404)


@pytest.mark.P1
@pytest.mark.Task
@pytest.mark.Mobile
def test_reopen_task(app, api, user):

    # Setup
    project_name = 'Setel Project3'
    task_title = 'testing 123'
    task_datetime = '26 June 2020 11am'
    token = api['token']
    project_url = api['project_url']
    project_task_url = api['project_task_url']
    email = user['email']
    password = user['password']
    project_id = api_create_new_project(token, project_url, project_name)
    assert (project_id > 0)

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
    time.sleep(3)

    task_id = api_get_project_task_id_by_name(token, project_task_url, project_id, task_title)
    app.back()

    time.sleep(5)
    left_nav.get_main_menu()
    time.sleep(3)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)
    project_page.mark_completed_project_task_by_name(task_title)
    time.sleep(5)

    api_reopen_task(token, project_task_url, task_id)
    TodoistGeneric.sync_data(app)

    time.sleep(5)
    left_nav.select_a_project_by_project_name(project_name)
    time.sleep(5)
    assert (project_page.get_project_task_by_name(task_title) is not None)

    # Teardown
    api_delete_project(token, project_url, project_id)
    response = api_get_project_details(token, project_url, project_id)
    assert (response.status_code == 404)