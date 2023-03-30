import pytest
from find_diff.gendiff import generate_diff
from find_diff.unpack_files import get_file_format, unpack_file
from find_diff.formaters.formater_json import get_diff_json
from find_diff.formaters.formater_plain import get_diff_plain
from find_diff.formaters.formater_stylish import get_diff_stylish
from find_diff.comparison import compare_dicts


TEST_FILES = {
    'json': ['tests/fixtures/file1.json',
             'tests/fixtures/file2.json'],
    'yaml': ['tests/fixtures/file1.yaml',
             'tests/fixtures/file2.yml'],
    'invalid': ['tests/fixtures/invalid_file.txt'],
    'non-existent': ['tests/fixtures/non_existent.txt']
}


TEST_DICTS = {
    'dict1': 'find_diff/tests/fixtures/file1.json',
    'dict2': 'find_diff/tests/fixtures/file2.json',
    'dict3': 'find_diff/tests/fixtures/file3.json',
    'dict4': 'find_diff/tests/fixtures/file4.json',
    'empty dict': 'find_diff/tests/fixtures/file5.json',
    'diff_dict': 'find_diff/tests/fixtures/diff_dict.txt',
    'not_diff_dict': 'find_diff/tests/fixtures/not_diff_dict.txt'
}


EXPECTED_VALUES = {
    'unpack_js': 'find_diff/tests/fixtures/'
                 'expected_value/unpack_js.txt',
    'unpack_yaml': 'find_diff/tests/fixtures/'
                   'expected_value/unpack_yaml.txt',
    'compare_empty_dict': 'find_diff/tests/fixtures/'
                          'expected_value/compare_empty_dict.txt',
    'compare_empty_from_dict': 'find_diff/tests/fixtures/expected'
                               '_value/compare_empty_from_dict.txt',
    'compare_same_dicts': 'find_diff/tests/fixtures/'
                          'expected_value/compare_same_dicts.txt',
    'compare_nested_dicts': 'find_diff/tests/fixtures/'
                            'expected_value/compare_nested_dicts.txt',
    'compare_flat_dicts': 'find_diff/tests/fixtures/'
                          'expected_value/compare_flat_dicts.txt',
    'for_js_empty_dicts': 'find_diff/tests/fixtures/'
                            'expected_value/for_js_empty_dicts.txt',
    'for_js_not_diff': 'find_diff/tests/fixtures/'
                         'expected_value/for_js_not_diff.txt',
    'for_js_diff_dict': 'find_diff/tests/fixtures/'
                          'expected_value/for_js_diff_dict.txt',
    'for_plain_empty_dicts': 'find_diff/tests/fixtures/'
                            'expected_value/for_plain_empty_dicts.txt',
    'for_plain_not_diff': 'find_diff/tests/fixtures/'
                         'expected_value/for_plain_not_diff.txt',
    'for_plain_diff_dict': 'find_diff/tests/fixtures/'
                          'expected_value/for_plain_diff_dict.txt',
    'for_stylish_empty_dicts': 'find_diff/tests/fixtures/'
                            'expected_value/for_stylish_empty_dicts.txt',
    'for_stylish_not_diff': 'find_diff/tests/fixtures/'
                         'expected_value/for_stylish_not_diff.txt',
    'for_stylish_diff_dict': 'find_diff/tests/fixtures/'
                          'expected_value/for_stylish_diff_dict.txt',
    'stylish_format': 'find_diff/tests/fixtures/'
                      'expected_value/stylish_format.txt',
    'plain_format': 'find_diff/tests/fixtures/'
                    'expected_value/plain_format.txt',
    'json_format': 'find_diff/tests/fixtures/'
                   'expected_value/json_format.txt',
    'json_file': 'find_diff/tests/fixtures/'
                 'expected_value/json_file.txt'
}


@pytest.fixture(params=TEST_DICTS)
def test_dicts(request):
    return TEST_DICTS[request.param]


@pytest.fixture(params=TEST_FILES)
def test_files(request):
    return TEST_FILES[request.param]


@pytest.fixture(params=EXPECTED_VALUES)
def expected_value(request):
    return EXPECTED_VALUES[request.param]


def read_txt_file(file_path):
    with open(file_path, "r") as file:
        contents = file.read()

    return contents


def test_get_file_json(test_files):
    assert get_file_format(test_files('json')[0]) == 'json'


def test_get_file_yaml(test_files):
    assert get_file_format(test_files('yaml')[0]) == 'yaml'
    assert get_file_format(test_files('yaml')[1]) == 'yml'


def test_get_file_error(test_files):
    with pytest.raises(ValueError):
        get_file_format(test_files('invalid')[0])


def test_unpack_file_js(test_files, expected_value):
    expected_value = read_txt_file(expected_value['unpack_js'])

    assert unpack_file(test_files('json')[0]) == expected_value


def test_unpack_file_yml(test_files, expected_value):
    expected_value = read_txt_file(expected_value['unpack_yaml'])

    assert unpack_file(test_files('yaml')[0]) == expected_value


def test_unpack_file_invalid(test_files):
    with pytest.raises(ValueError):
        unpack_file(test_files('invalid')[0])


def test_unpack_file_invalid(test_files):

    with pytest.raises(FileNotFoundError):
        unpack_file(test_files('non-existent')[0])


def test_compare_dicts_empty_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['compare_empty_dict'])
    empty_dict = unpack_file(test_dicts('empty_dict'))

    assert compare_dicts(empty_dict, empty_dict) == expected_value


def test_compare_dicts_empty_dict_from_dict(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['compare_empty_from_dict'])
    empty_dict = unpack_file(test_dicts('empty_dict'))
    dic = unpack_file(test_dicts('dict1'))

    assert compare_dicts(empty_dict, dic) == expected_value


def test_compare_dicts_same_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['compare_same_dicts'])
    dic1 = unpack_file(test_dicts('dict1'))
    dic2 = unpack_file(test_dicts('dict1'))

    assert compare_dicts(dic1, dic2) == expected_value


def test_compare_dicts_nested_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['compare_nested_dicts'])
    dic1 = unpack_file(test_dicts('dict3'))
    dic2 = unpack_file(test_dicts('dict4'))

    assert compare_dicts(dic1, dic2) == expected_value


def test_compare_dicts_flat_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['compare_flat_dicts'])
    dic1 = unpack_file(test_dicts('dict1'))
    dic2 = unpack_file(test_dicts('dict2'))

    assert compare_dicts(dic1, dic2) == expected_value

#get_diff_json

def test_get_diff_json_empty_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_js_empty_dicts'])
    empty_dict = unpack_file(test_dicts('empty_dict'))

    assert get_diff_json(empty_dict) == expected_value


def test_get_diff_json_not_diff(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_js_not_diff'])
    not_diff_dict = read_txt_file(test_dicts('not_diff_dict'))

    assert get_diff_json(not_diff_dict) == expected_value


def test_get_diff_json_diff_dict(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_js_diff_dict'])
    diff_dict = read_txt_file(test_dicts('diff_dict'))

    assert get_diff_json(diff_dict) == expected_value

#get_diff_plain

def test_get_diff_plain_empty_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_plain_empty_dicts'])
    empty_dict = unpack_file(test_dicts('empty_dict'))

    assert get_diff_plain(empty_dict) == expected_value


def test_get_diff_plain_not_diff(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_plain_not_diff'])
    not_diff_dict = read_txt_file(test_dicts('not_diff_dict'))

    assert get_diff_plain(not_diff_dict) == expected_value


def test_get_diff_plain_diff_dict(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_plain_diff_dict'])
    diff_dict = read_txt_file(test_dicts('diff_dict'))

    assert get_diff_plain(diff_dict) == expected_value

#get_diff_stylish

def test_get_diff_stylish_empty_dicts(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_stylish_empty_dicts'])
    empty_dict = unpack_file(test_dicts('empty_dict'))

    assert get_diff_stylish(empty_dict) == expected_value


def test_get_diff_stylish_not_diff(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_stylish_not_diff'])
    not_diff_dict = read_txt_file(test_dicts('not_diff_dict'))

    assert get_diff_stylish(not_diff_dict) == expected_value


def test_get_diff_stylish_diff_dict(test_dicts, expected_value):
    expected_value = read_txt_file(expected_value['for_stylish_diff_dict'])
    diff_dict = read_txt_file(test_dicts('diff_dict'))

    assert get_diff_stylish(diff_dict) == expected_value


def test_generate_diff_stylish_format(test_files, expected_value):
    expected_value = read_txt_file(expected_value['stylish_format'])
    file1 = unpack_file(test_dicts(test_files('json')[0]))
    file2 = unpack_file(test_dicts(test_files('json')[1]))

    assert generate_diff(file1, file2) == expected_value


def test_generate_diff_plain_format(test_files, expected_value):
    expected_value = read_txt_file(expected_value['plain_format'])
    file1 = unpack_file(test_dicts(test_files('json')[0]))
    file2 = unpack_file(test_dicts(test_files('json')[1]))

    assert generate_diff(file1, file2, 'plain') == expected_value


def test_generate_diff_json_format(test_files, expected_value):
    expected_value = read_txt_file(expected_value['json_format'])
    file1 = unpack_file(test_dicts(test_files('json')[0]))
    file2 = unpack_file(test_dicts(test_files('json')[1]))

    assert generate_diff(file1, file2, 'json') == expected_value

def test_generate_diff_yml_file(test_files, expected_value):
    expected_value = read_txt_file(expected_value['json_file'])
    file1 = unpack_file(test_dicts(test_files('yaml')[0]))
    file2 = unpack_file(test_dicts(test_files('yaml')[1]))

    assert generate_diff(file1, file2, 'json') == expected_value


def test_generate_diff_with_unsupported_format(test_files):
    file1 = unpack_file(test_dicts(test_files('json')[0]))
    file2 = unpack_file(test_dicts(test_files('json')[1]))
    with pytest.raises(ValueError):
        generate_diff(file1, file2, 'unsupported_format')
