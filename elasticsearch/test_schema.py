import pytest
import os
import json
import pytest
import allure

from util.es import es_connect
from util.fileaccess import load_csv_to_dict, load_json_file


INDEX_TEST_DATA_PATH = 'data\\es\\schema\\index.csv'
KNOWN_SYSTEM_INDEX_DATA_PATH = 'data\\es\\schema\\known_system_index.csv'


# Loads and return expected index data
def get_index_data():
    index_test_data = load_csv_to_dict(INDEX_TEST_DATA_PATH)
    return index_test_data


# Loads and return known system index data
def get_known_system_index_data():
    return load_csv_to_dict(KNOWN_SYSTEM_INDEX_DATA_PATH)


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Settings
@pytest.mark.parametrize(
    'data', get_index_data())
@allure.epic('ElasticSearch - Index')
@allure.feature('Feature - Index setting')
@allure.story('Story - Check Index setting')
@allure.testcase('Test Case  - Check index setting')
def test_index_settings(es, data):
    settings = es.indices.get_settings(data['index'])

    # Getting actual no of replicas and shards for the index
    actual_no_replicas = \
        settings[data['index']]['settings']['index']['number_of_replicas']
    actual_no_shards = \
        settings[data['index']]['settings']['index']['number_of_shards']

    # Getting expected no of replicas and shards for the index
    expected_no_replicas = data['no_replicas']
    expected_no_shards = data['no_shards']

    # Comparing if actual value is equal to expected value
    assert actual_no_replicas == expected_no_replicas
    assert actual_no_shards == expected_no_shards


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Mappings
@pytest.mark.parametrize(
    'data', get_index_data())
@allure.epic('ElasticSearch - Index')
@allure.feature('Feature - Index mapping')
@allure.story('Story - Check index mapping')
@allure.testcase('Test Case  - Check index mapping')
def test_index_mappings(es, data):

    actual_mapping = es.indices.get_mapping(data['index'])
    expected_mapping = load_json_file(data['mapping'])

    # Compare if the actual index mapping is equal to expected mapping
    assert actual_mapping == expected_mapping


@pytest.mark.P1
@pytest.mark.Index
@allure.epic('ElasticSearch - Index')
@allure.feature('Feature - Index core')
@allure.story('Story - Check index')
@allure.testcase('Test Case  - Check if there is extra Index')
def test_check_if_there_is_extra_index(es):
    all_indexes = es.indices.get_alias("*").keys()
    expected_data = get_index_data()
    known_system_index = get_known_system_index_data()
    extra_index_list = []
    expected_indexes = []
    expected_known_system_index = []

    # Loads expected indexes
    for data in expected_data:
        expected_indexes.append(data['index'])

    # Loads known system indexes
    for data in known_system_index:
        expected_known_system_index.append(data['index'])

    # Identify and loads extra indexes if actual index is not in expected
    # and known system index
    for actual_index in all_indexes:
        if actual_index not in expected_indexes:
            if actual_index not in expected_known_system_index:
                extra_index_list.append(actual_index)

    print('Extra Index')
    print('=============')
    print(extra_index_list)

    # Check if there is extra index in actual environment
    assert len(extra_index_list) == 0