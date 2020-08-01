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


def query_construct(fieldnames, data):
    match = []
    for field in fieldnames:
        if field == "email":
            match.append(Q('match', email=data['email']))
        if field == "user_name":
            match.append(Q('match', user_name=data['user_name']))
        if field == "first_name":
            match.append(Q('match', first_name=data['first_name']))
        if field == "last_name":
            match.append(Q('match', last_name=data['last_name']))
        if field == "country":
            match.append(Q('match', country=data['country']))
    return match



@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Users
@pytest.mark.parametrize(
    'data', get_execution_data())
@allure.epic("ElasticSearch - Index")
@allure.feature("Feature - User index")
@allure.story("Story - Check user data")
@allure.testcase("Test Case  - Check missing users")
def test_checking_of_missing_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'add':
            test_data = load_csv_to_dict(data['datafile'])
            for user in test_data:
                user_count += 1
                query = query_construct(test_data.fieldnames, user)
                q = Q('bool', must=query)
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
@allure.feature("Feature - User index")
@allure.story("Story - Check user data")
@allure.testcase("Test Case  - Check deleted users")
def test_checking_of_deleted_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'delete':
            test_data = load_csv_to_dict(data['datafile'])
            for user in test_data:
                user_count += 1
                query = query_construct(test_data.fieldnames, user)
                q = Q('bool', must=query)
                s = Search(using=es, index='users')
                s = s.query(q)
                response = s.execute()
                print(response)
                for hit in response:
                    hit_count += 1
        assert hit_count == 0
