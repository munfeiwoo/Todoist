import pytest
import os
import json
import pytest
import logging
import allure

from util.es import es_connect, es_search
from util.fileaccess import load_csv_to_dict, load_json_file
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

DATA_VERIFICATION_EXECUTION_PATH = 'elasticsearch\\data_verification_execution.csv'


def get_execution_data():
    test_execution_data = load_csv_to_dict(DATA_VERIFICATION_EXECUTION_PATH)
    return test_execution_data


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Users
@pytest.mark.parametrize(
    'data', get_execution_data())
@allure.epic("ElasticSearch - Index")
@allure.feature("Feature 001")
@allure.story("Story 001")
@allure.testcase("Test Case 001")
def test_checking_of_missing_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'add':
            test_data = load_csv_to_dict(data['datafile'])
            for user in test_data:
                user_count += 1
                q = Q('bool',
                      must=[Q('match', email=user['email']),
                            Q('match', user_name=user['user_name']),
                            Q('match', first_name=user['first_name']),
                            Q('match', last_name=user['last_name'])
                            ]
                      )
                s = Search(using=es, index='users')
                s = s.query(q)
                response = s.execute()
                print(response)
                for hit in response:
                    hit_count += 1
    assert user_count == hit_count


@pytest.mark.P2
@pytest.mark.Index
@pytest.mark.Users
@pytest.mark.parametrize(
    'data', get_execution_data())
@allure.epic("ElasticSearch - Index")
@allure.feature("Feature 002")
@allure.story("Story 002")
@allure.testcase("Test Case 002")
def test_checking_of_deleted_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'delete':
            test_data = load_csv_to_dict(data['datafile'])
            for user in test_data:
                user_count += 1
                q = Q('bool',
                      must=[Q('match', email=user['email']),
                            Q('match', user_name=user['user_name']),
                            Q('match', first_name=user['first_name']),
                            Q('match', last_name=user['last_name'])
                            ]
                      )
                s = Search(using=es, index='users')
                s = s.query(q)
                response = s.execute()
                print(response)
                for hit in response:
                    hit_count += 1
        assert hit_count == 0
