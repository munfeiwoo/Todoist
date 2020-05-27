import uuid
import requests
import json
import time
import pytest


def api_create_new_project(token, project_url, project_name):
    response = requests.post(
        project_url,
        data=json.dumps({
            "name": project_name
        }),
        headers={
            "Content-Type": "application/json",
            "X-Request-Id": str(uuid.uuid4()),
            "Authorization": "Bearer {}".format(token)
        })
    assert response.status_code == 200,  'Response status should be 200'
    project = response.json()
    assert (project['name'] == project_name)
    return project['id']


def api_delete_project(token, project_url, project_id):
    response = requests.delete(project_url + "/{}".format(project_id),
                               headers={"Authorization": "Bearer {}".format(token)})
    assert response.status_code == 204, 'Response status should be 204'


def api_get_project_details(token, project_url, project_id):
    response = requests.get(project_url + "/{}".format(project_id),
                            headers={"Authorization": "Bearer {}".format(token)})
    return response


def api_get_all_projects(token, project_url):
    response = requests.get(project_url,
                            headers={"Authorization": "Bearer {}".format(token)}).json()
    return response


def api_get_project_id_by_project_name(token, project_url, project_name):
    projects = api_get_all_projects(token, project_url)
    for project in projects:
        if project['name'] == project_name:
            return project['id']


def api_get_project_ids_by_project_name(token, project_url, project_name):
    projects = api_get_all_projects(token, project_url)
    projects_list = []
    for project in projects:
        if project['name'] == project_name:
            projects_list.append(project['id'])
    return projects_list


def api_remove_projects_by_project_name(token, project_url, project_name):
    project_ids = api_get_project_ids_by_project_name(token, project_url, project_name)
    for project_id in project_ids:
        api_delete_project(token, project_url, project_id)
        # Verify if project deleted
        response = api_get_project_details(token, project_url, project_id)
        assert response.status_code == 404, 'Response status should be 404'


def api_remove_project_by_project_id(token, project_url, project_id):
    api_delete_project(token, project_url, project_id)
    # Verify if project deleted
    response = api_get_project_details(token, project_url, project_id)
    assert response.status_code == 404, 'Response status should be 404'


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.API
def test_create_and_delete_project(api_test_config):
    project_name = "project3"
    token = api_test_config['api_token']
    project_url = api_test_config['api_project_url']
    project_id = api_create_new_project(token, project_url, project_name)
    assert project_id is not None, 'Project id should not be None'
    time.sleep(10)

    api_remove_project_by_project_id(token, project_url, project_id)


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.API
def test_remove_all_projects_by_project_name(api_test_config):
    project_name = "sample1"
    token = api_test_config['api_token']
    project_url = api_test_config['api_project_url']
    x = range(2)
    for n in x:
        project_id = api_create_new_project(token, project_url, project_name)
        assert project_id is not None, 'Project id should not be None'
    api_remove_projects_by_project_name(token, project_url, project_name)
