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
    assert (response.status_code == 200)
    project = response.json()
    assert (project['name'] == project_name)
    return project['id']


def api_delete_project(token, project_url, project_id):
    response = requests.delete(project_url + "/{}".format(project_id),
                               headers={"Authorization": "Bearer {}".format(token)})
    assert (response.status_code == 204)


def api_get_project_details(token, project_url, project_id):
    response = requests.get(project_url + "/{}".format(project_id),
                            headers={"Authorization": "Bearer {}".format(token)})
    return response


@pytest.mark.P1
@pytest.mark.Project
@pytest.mark.API
def test_create_and_delete_project(api_test_config):
    project_name = "project3"
    token = api_test_config['token']
    project_url = api_test_config['project_url']
    project_id = api_create_new_project(token, project_url, project_name)
    assert (project_id > 0)
    time.sleep(10)

    api_delete_project(token, project_url, project_id)
    response = api_get_project_details(token, project_url, project_id)
    assert (response.status_code == 404)
