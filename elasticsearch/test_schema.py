import pytest
import os
import json
import pytest
import logging

from util.es import es_connect
from util.fileaccess import load_csv_to_dict, load_json_file

logging.basicConfig(level=logging.DEBUG)
log = logging.getLogger()

INDEX_TEST_DATA_PATH = 'data\\es\\schema\\index.csv'
KNOWN_SYSTEM_INDEX_DATA_PATH = 'data\\es\\schema\\known_system_index.csv'


def get_index_data():
    index_test_data = load_csv_to_dict(INDEX_TEST_DATA_PATH)
    return index_test_data


def get_known_system_index_data():
    return load_csv_to_dict(KNOWN_SYSTEM_INDEX_DATA_PATH)


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Settings
@pytest.mark.parametrize(
    'data', get_index_data())
def test_index_settings(es, data):
    settings = es.indices.get_settings(data['index'])
    actual_no_replicas = \
        settings[data['index']]['settings']['index']['number_of_replicas']
    actual_no_shards = \
        settings[data['index']]['settings']['index']['number_of_shards']
    expected_no_replicas = data['no_replicas']
    expected_no_shards = data['no_shards']
    assert actual_no_replicas == expected_no_replicas
    assert actual_no_shards == expected_no_shards


@pytest.mark.P1
@pytest.mark.Index
@pytest.mark.Mappings
@pytest.mark.parametrize(
    'data', get_index_data())
def test_index_mappings(es, data):
    actual_mapping = es.indices.get_mapping(data['index'])
    expected_mapping = load_json_file(data['mapping'])
    assert actual_mapping == expected_mapping


@pytest.mark.P1
@pytest.mark.Index
def test_check_if_there_is_extra_index(es):
    all_indexes = es.indices.get_alias("*").keys()
    expected_data = get_index_data()
    known_system_index = get_known_system_index_data()
    extra_index_list = []
    expected_indexes = []
    expected_known_system_index = []

    for data in expected_data:
        expected_indexes.append(data['index'])

    for data in known_system_index:
        expected_known_system_index.append(data['index'])

    for actual_index in all_indexes:
        if actual_index not in expected_indexes:
            if actual_index not in expected_known_system_index:
                extra_index_list.append(actual_index)


    print('Extra Index')
    print('============')
    print(extra_index_list)
    assert len(extra_index_list) == 0
