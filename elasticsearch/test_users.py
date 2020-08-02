import pytest
import os
import json
import pytest
import logging
import allure

from util.es import es_connect
from util.fileaccess import load_csv_to_dict, load_json_file
from elasticsearch_dsl import Search
from elasticsearch_dsl import Q

ADDED_USERS_DATA_VERIFICATION_EXECUTION_PATH = 'elasticsearch\\execution\\added_users_data_verification.csv'
DELETED_USERS_DATA_VERIFICATION_EXECUTION_PATH = 'elasticsearch\\execution\\deleted_users_data_verification.csv'


# Loads and return execution data for expected added users
def get_execution_data_for_added_users():
    test_execution_data = load_csv_to_dict(ADDED_USERS_DATA_VERIFICATION_EXECUTION_PATH)
    return test_execution_data


# Loads and return execution data for expected deleted users
def get_execution_data_for_deleted_users():
    test_execution_data = load_csv_to_dict(DELETED_USERS_DATA_VERIFICATION_EXECUTION_PATH)
    return test_execution_data


# Dynamically construct match query for each fields and data provided
def query_construct(fieldnames, data):
    match = []
    for field in fieldnames:
        if field == 'email':
            match.append(Q('match', email=data['email']))
        if field == 'user_name':
            match.append(Q('match', user_name=data['user_name']))
        if field == 'first_name':
            match.append(Q('match', first_name=data['first_name']))
        if field == 'last_name':
            match.append(Q('match', last_name=data['last_name']))
        if field == 'country':
            match.append(Q('match', country=data['country']))
    return match


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Users
@pytest.mark.parametrize(
    'data', get_execution_data_for_added_users())
@allure.epic('ElasticSearch - Users')
@allure.feature('Feature - User index')
@allure.story('Story - Check user data')
@allure.testcase('Test Case  - Check missing users')
def test_checking_of_missing_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'add':

            # Loads user data
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

    # Check if the expected user count is equal to the actual user count
    assert user_count == hit_count, \
        'Expected {} users but ES returning {} users'.format(user_count, hit_count)


@pytest.mark.P2
@pytest.mark.Index
@pytest.mark.Users
@pytest.mark.parametrize(
    'data', get_execution_data_for_deleted_users())
@allure.epic('ElasticSearch - Users')
@allure.feature('Feature - User index')
@allure.story('Story - Check user data')
@allure.testcase('Test Case  - Check deleted users')
def test_checking_of_deleted_user(es, data):
    user_count = 0
    hit_count = 0
    if data['index'] == 'users':
        if data['action'] == 'delete':

            # Loads user data
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

        # Check if the expected user count is equal to the actual user count
        assert hit_count == 0, \
            'Expected 0 user but ES returning {} users'.format(hit_count)