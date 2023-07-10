import pytest
import os
import json
import yaml
from gendiff.formaters.convert_bool import convert_dict_values
from gendiff.gendiff import generate_diff
from gendiff.unpack_files import get_file_format, unpack_file
from gendiff.formaters.formater_json import get_diff_json
from gendiff.formaters.formater_plain import get_diff_plain
from gendiff.formaters.formater_stylish import get_diff_stylish
from gendiff.comparison import compare_dicts


EXPECTED_VALUES_PATH = os.getcwd() + '/tests/fixtures/expected_value/'
PASSED_VALUES_PATH = os.getcwd() + '/tests/fixtures/passed_value/'


TEST_FILES = {
    'file1_js': 'file1.json',
    'file2_js': 'file2.json',
    'file3_js': 'file3.json',
    'file4_js': 'file4.json',
    'file5_js': 'file5.json',
    'file1_yaml': 'file1.yaml',
    'file2_yml': 'file2.yml',
    'invalid_file': 'invalid_file.txt',
    'non_existent': 'non_existent.txt',
    'diff_dict': 'diff_dict.json',
    'not_diff_dict': 'not_diff_dict.json'
}


EXPECTED_VALUES = {
    'unpack': 'unpack.txt',
    'compare_empty': 'compare_empty_from_dict.txt',
    'compare_same': 'compare_same_dicts.txt',
    'compare_nested': 'compare_nested_dicts.txt',
    'compare_flat': 'compare_flat_dicts.txt',
    'js_empty': 'for_js_empty_dicts.txt',
    'js_not_diff': 'for_js_not_diff.txt',
    'js_diff': 'for_js_diff_dict.txt',
    'plain_empty': 'for_plain_empty.txt',
    'plain_not_diff': 'for_plain_not_diff.txt',
    'plain_diff': 'for_plain_diff.txt',
    'stylish_empty': 'for_stylish_empty.txt',
    'stylish_not_diff': 'for_stylish_not_diff.txt',
    'stylish_diff': 'for_stylish_diff.txt',
    'stylish_format': 'stylish_format.txt',
    'plain_format': 'plain_format.txt',
    'json_format': 'json_format.txt',
    'yaml_file': 'yaml_file.txt',
    'convert_flat': 'convert_flat.txt',
    'convert_nasted': 'convert_nasted.txt',
    'empty_dict': 'empty_dict.txt'
}


def read_txt_file(file_path: str):
    file_path = EXPECTED_VALUES_PATH + file_path
    with open(file_path, "r") as file:
        contents = file.read()

    return contents


def unpack_tests_file(file_path: str):
    file_path = PASSED_VALUES_PATH + file_path
    with open(file_path) as file:
        format = get_file_format(file_path)
        if format == 'json':
            content = json.load(file, parse_constant=lambda x: x)
        elif format == 'yaml':
            content = yaml.safe_load(file)

        return content


@pytest.mark.parametrize('test_file, expected_value',
                         [(TEST_FILES['file1_js'], 'json'),
                          (TEST_FILES['file1_yaml'], 'yaml'),
                          (TEST_FILES['file2_yml'], 'yaml')])
def test_get_file_format(test_file, expected_value):
    assert get_file_format(test_file) == expected_value


def test_get_file_error():
    with pytest.raises(ValueError):
        get_file_format(TEST_FILES['invalid_file'])


@pytest.mark.parametrize('path, expected_value',
                         [(TEST_FILES['file1_js'],
                           EXPECTED_VALUES['unpack']),
                          (TEST_FILES['file1_yaml'],
                           EXPECTED_VALUES['unpack'])])
def test_unpack_file(path, expected_value):
    path = PASSED_VALUES_PATH + path
    expected_value = read_txt_file(expected_value)
    assert unpack_file(path) == eval(expected_value)


@pytest.mark.parametrize('dic1, dic2, expected_value',
                         [(TEST_FILES['file5_js'],
                           TEST_FILES['file5_js'],
                           EXPECTED_VALUES['empty_dict']),
                          (TEST_FILES['file5_js'],
                           TEST_FILES['file1_js'],
                           EXPECTED_VALUES['compare_empty']),
                          (TEST_FILES['file1_js'],
                           TEST_FILES['file1_js'],
                           EXPECTED_VALUES['compare_same']),
                          (TEST_FILES['file3_js'],
                           TEST_FILES['file4_js'],
                           EXPECTED_VALUES['compare_nested']),
                          (TEST_FILES['file1_js'],
                           TEST_FILES['file2_js'],
                           EXPECTED_VALUES['compare_flat'])])
def test_compare_dicts(dic1, dic2, expected_value):
    dic1 = unpack_tests_file(dic1)
    dic2 = unpack_tests_file(dic2)
    expected_value = eval(read_txt_file(expected_value))
    assert compare_dicts(dic1, dic2) == expected_value


@pytest.mark.parametrize('diff_dict, expected_value',
                         [(TEST_FILES['file5_js'],
                           EXPECTED_VALUES['js_empty']),
                          (TEST_FILES['not_diff_dict'],
                           EXPECTED_VALUES['js_not_diff']),
                          (TEST_FILES['diff_dict'],
                           EXPECTED_VALUES['js_diff'])])
def test_get_diff_json(diff_dict, expected_value):
    diff_dict = unpack_tests_file(diff_dict)
    expected_value = read_txt_file(expected_value)
    assert get_diff_json(diff_dict) == expected_value


@pytest.mark.parametrize('diff_dict, expected_value',
                         [(TEST_FILES['file5_js'],
                           EXPECTED_VALUES['plain_empty']),
                          (TEST_FILES['not_diff_dict'],
                           EXPECTED_VALUES['plain_not_diff']),
                          (TEST_FILES['diff_dict'],
                           EXPECTED_VALUES['plain_diff'])])
def test_get_diff_plain(diff_dict, expected_value):
    diff_dict = unpack_tests_file(diff_dict)
    expected_value = read_txt_file(expected_value)
    assert get_diff_plain(diff_dict) == expected_value


@pytest.mark.parametrize('diff_dict, expected_value',
                         [(TEST_FILES['file5_js'],
                           EXPECTED_VALUES['stylish_empty']),
                          (TEST_FILES['not_diff_dict'],
                           EXPECTED_VALUES['stylish_not_diff']),
                          (TEST_FILES['diff_dict'],
                           EXPECTED_VALUES['stylish_diff'])])
def test_get_diff_stylish(diff_dict, expected_value):
    diff_dict = unpack_tests_file(diff_dict)
    expected_value = read_txt_file(expected_value)
    assert get_diff_stylish(diff_dict) == expected_value


@pytest.mark.parametrize('format, expected_value',
                         [('stylish', EXPECTED_VALUES['stylish_format']),
                          ('plain', EXPECTED_VALUES['plain_format']),
                          ('json', EXPECTED_VALUES['json_format'])])
def test_generate_diff_json_file(format, expected_value):
    file1 = (PASSED_VALUES_PATH + TEST_FILES['file1_js'])
    file2 = (PASSED_VALUES_PATH + TEST_FILES['file2_js'])
    expected_value = read_txt_file(expected_value)
    assert generate_diff(file1, file2, format) == expected_value


def test_generate_diff_yaml_file():
    file1 = (PASSED_VALUES_PATH + TEST_FILES['file1_yaml'])
    file2 = (PASSED_VALUES_PATH + TEST_FILES['file2_yml'])
    expected_value = read_txt_file(EXPECTED_VALUES['yaml_file'])
    assert generate_diff(file1, file2, 'json') == expected_value


def test_generate_diff_unsupported_format():
    file1 = (PASSED_VALUES_PATH + TEST_FILES['file1_js'])
    file2 = (PASSED_VALUES_PATH + TEST_FILES['file2_js'])
    with pytest.raises(ValueError):
        generate_diff(file1, file2, 'unsupported_format')


@pytest.mark.parametrize('dic, expacted_value',
                         [(TEST_FILES['file1_js'],
                           EXPECTED_VALUES['convert_flat']),
                          (TEST_FILES['file3_js'],
                           EXPECTED_VALUES['convert_nasted'])])
def test_convert_dict_values(dic, expacted_value):
    dic = unpack_tests_file(dic)
    expected_value = eval(read_txt_file(expacted_value))

    assert convert_dict_values(dic) == expected_value
