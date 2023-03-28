import pytest
import os
import json
from find_diff.gendiff import generate_diff
from find_diff.unpack_files import get_file_format, unpack_file
from find_diff.formaters.formater_json import get_diff_json
from find_diff.formaters.formater_plain import get_diff_plain
from find_diff.formaters.formater_stylish import get_diff_stylish
from find_diff.comparison import compare_dicts


TEST_FILES = {
    'json': ['tests/fixtures/1.json', 'tests/fixtures/2.json',
             'tests/fixtures/3.json', 'tests/fixtures/4.json'],
    'yaml': ['tests/fixtures/1.yaml', 'tests/fixtures/2.yaml',
             'tests/fixtures/3.yaml', 'tests/fixtures/4.yaml']
}


TEST_FORMATS = {'stylish': 'tests/fixtures/correct.txt',
                'plain': 'tests/fixtures/correct_plain.txt',
                'json': 'tests/fixtures/correct_json.txt'}


@pytest.fixture(params=TEST_FILES)
def test_files(request):
    return TEST_FILES[request.param]


@pytest.fixture(params=TEST_FORMATS)
def test_format(request):
    return TEST_FILES[request.param]


def test_get_file_format(test_files):
    # Test JSON file format
    assert get_file_format(test_files('json')[0]) == 'json'

    # Test YAML file format
    assert get_file_format('/path/to/file.yaml') == 'yaml'
    assert get_file_format('/path/to/file.yml') == 'yaml'

    # Test unrecognized file format
    with pytest.raises(ValueError):
        get_file_format('/path/to/file.txt')


JSON_PATH = '/path/to/test.json'
YAML_PATH = '/path/to/test.yaml'
INVALID_PATH = '/path/to/test.txt'
NONEXISTENT_PATH = '/path/to/nonexistent/file'

def test_unpack_file():
    # Test JSON file format
    assert unpack_file(JSON_PATH) == {'key': 'value'}

    # Test YAML file format
    assert unpack_file(YAML_PATH) == {'key': 'value'}

    # Test invalid file format
    with pytest.raises(ValueError):
        unpack_file(INVALID_PATH)

    # Test non-existent file
    with pytest.raises(FileNotFoundError):
        unpack_file(NONEXISTENT_PATH)


# Test for when both dictionaries are empty
empty_dict1 = {}
empty_dict2 = {}
empty_dict_result = {}
# Test for when one of the dictionaries is empty
dict1 = {'key1': 'value1', 'key2': {'nested_key1': 'nested_value1'}}
dict2 = {}
empty_dict_from_dict2_result = {'key1': {'dict1': 'value1'}, 'key2': {'dict1': {'nested_key1': 'nested_value1'}}}
# Test for when both dictionaries are the same
same_dict1 = {'key1': 'value1', 'key2': {'nested_key1': 'nested_value1'}}
same_dict2 = {'key1': 'value1', 'key2': {'nested_key1': 'nested_value1'}}
same_dict_result = {}
# Test for when one of the dictionaries has nested dictionaries but the other doesn't
nested_dict1 = {'key1': {'nested_key1': 'nested_value1'}, 'key2': 'value2'}
nested_dict2 = {'key1': 'value1', 'key2': {'nested_key1': 'nested_value1'}}
nested_dict_result = {'key1': {'dict1': {'nested_key1': 'nested_value1'}, 'dict2': 'value1'}, 'key2': {'dict1': 'value2', 'dict2': {'nested_key1': 'nested_value1'}}}
# Test for when both dictionaries have nested dictionaries with different levels of nesting
diff_nested_dict1 = {'key1': {'nested_key1': 'nested_value1', 'nested_key2': {'nested_key3': 'nested_value3'}}, 'key2': 'value2'}
diff_nested_dict2 = {'key1': {'nested_key1': 'nested_value1', 'nested_key2': {'nested_key3': 'nested_value4'}}, 'key3': {'nested_key4': 'nested_value5'}}
diff_nested_dict_result = {'key1': {'nested_key2': {'nested_key3': {'dict1': 'nested_value3', 'dict2': 'nested_value4'}}}, 'key2': {'dict1': 'value2'}, 'key3': {'dict2': {'nested_key4': 'nested_value5'}}}

def test_compare_dicts_empty_dicts():
    assert compare_dicts(empty_dict1, empty_dict2) == empty_dict_result

def test_compare_dicts_empty_dict_from_dict2():
    assert compare_dicts(dict1, empty_dict2) == empty_dict_from_dict2_result

def test_compare_dicts_same_dicts():
    assert compare_dicts(same_dict1, same_dict2) == same_dict_result

def test_compare_dicts_nested_dicts_with_missing_keys():
    assert compare_dicts(nested_dict1, nested_dict2) == nested_dict_result

def test_compare_dicts_nested_dicts_with_different_values():
    assert compare_dicts(diff_nested_dict1, diff_nested_dict2) == diff_nested_dict_result

#get_diff_json

def test_get_diff_json_empty_dicts():
    assert compare_dicts(empty_dict) == empty_dict_result


def test_get_diff_json_not_diff():
    assert compare_dicts(not_diff_dict) == not_diff_result


def test_get_diff_json_nested_dict():
    assert compare_dicts(nested_dict) == nested_dict_result


def test_get_diff_json_flat_dict():
    assert compare_dicts(flat_dict) == flat_dict_result

#get_diff_plain

def test_get_diff_plain_empty_dicts():
    assert compare_dicts(empty_dict) == empty_dict_result


def test_get_diff_plain_not_diff():
    assert compare_dicts(not_diff_dict) == not_diff_result


def test_get_diff_plain_nested_dict():
    assert compare_dicts(nested_dict) == nested_dict_result


def test_get_diff_plain_flat_dict():
    assert compare_dicts(flat_dict) == flat_dict_result

#get_diff_stylish

def test_get_diff_stylish_empty_dicts():
    assert compare_dicts(empty_dict) == empty_dict_result


def test_get_diff_stylish_not_diff():
    assert compare_dicts(not_diff_dict) == not_diff_result


def test_get_diff_stylish_nested_dict():
    assert compare_dicts(nested_dict) == nested_dict_result


def test_get_diff_stylish_flat_dict():
    assert compare_dicts(flat_dict) == flat_dict_result


#gendiff

def test_generate_diff_with_stylish_format():
    expected_output = '    common:\n      setting1: Value 1\n+     setting2: 200\n      setting3:\n        key: value\n-     setting4: blah blah\n    group1:\n      abc: 12345\n+     def: {\n+         ghi: {\n+           jkl: 123\n+         }\n+       }\n    group2:\n-     some_key: some_value\n+     some_key: {\n+       nested: {\n+         value: 5\n+       }\n+     }\n'
    assert generate_diff(file_path1, file_path2) == expected_output

def test_generate_diff_with_plain_format():
    expected_output = 'Property common.setting1 was updated. From Value 1 to Value 2\nProperty common.setting4 was removed\nProperty common.setting2 was added with value: 200\nProperty group1.abc was updated. From 12345 to 54321\nProperty group2.some_key was updated. From some_value to {\n  nested: {\n    value: 5\n  }\n}\n'
    assert generate_diff(file_path1, file_path2, 'plain') == expected_output

def test_generate_diff_with_json_format():
    expected_output = '{"common": {"setting1": "Value 1", "setting2": 200, "setting3": {"key": "value"}, "setting4": null}, "group1": {"abc": 12345, "def": {"ghi": {"jkl": 123}}}, "group2": {"some_key": {"nested": {"value": 5}}}}'
    assert generate_diff(file_path1, file_path2, 'json') == expected_output

def test_generate_diff_with_unsupported_format():
    with pytest.raises(ValueError):
        generate_diff(file_path1, file_path2, 'unsupported_format')

def test_generate_diff_with_different_file_types():
    with pytest.raises(TypeError):
        generate_diff(file_path1, file_path3)
