import pytest
from find_diff.gendiff import generate_diff, unpack_json, compare_dicts
from fixtures.fixtures_json import sample_data, sample_files, non_existent_file_json
from fixtures.fixtures_json import exp_val_dicts_identical, exp_val_dicts_different, exp_val_dicts_empty
from fixtures.fixtures_json import exp_val_identical_files, exp_val_empty_file, exp_val_different_files


def test_unpack_json_valid_file(sample_data, sample_files):
    # Test that the function correctly reads the contents of a valid JSON file
    # and returns the corresponding Python object.

    data = sample_data[0]
    file_path = sample_files[0]

    assert unpack_json(file_path) == data


def test_unpack_json_invalid_file(sample_files):
    # Test that the function raises a ValueError with invalid content

    file_path = sample_files[3]

    with pytest.raises(ValueError, match=f"{file_path} is not a valid JSON file"):
        unpack_json(file_path)


def test_unpack_json_invalid_path(sample_data):
    # Test that the function raises a FileNotFoundError with invalid path

    file_path = sample_data[3]

    with pytest.raises(FileNotFoundError, match=f"{file_path} does not exist"):
        unpack_json(file_path)


def test_unpack_json_non_existent_file(non_existent_file_json):
    # Test that the function raises a
    # FileNotFoundError with a non-existent file
    non_existent_file = non_existent_file_json

    with pytest.raises(FileNotFoundError):
        unpack_json(non_existent_file)


def test_compare_dicts_identical(sample_data, exp_val_dicts_identical):
    result = compare_dicts(sample_data[0], sample_data[0])
    expected_value = exp_val_dicts_identical

    assert result == expected_value


def test_compare_dicts_different(sample_data, exp_val_dicts_different):
    result = compare_dicts(sample_data[0], sample_data[1])
    expected_value = exp_val_dicts_different

    assert result == expected_value


def test_compare_dicts_empty(sample_data, exp_val_dicts_empty):
    result1 = compare_dicts(sample_data[0], sample_data[2])
    result2 = compare_dicts(sample_data[2], sample_data[0])

    assert result1 == exp_val_dicts_empty[0]
    assert result2 == exp_val_dicts_empty[1]


def test_generate_diff_non_existent_file(sample_files, non_existent_file_json):
    file_path = sample_files[0]
    non_existent_file = non_existent_file_json

    with pytest.raises(FileNotFoundError):
        generate_diff(file_path, non_existent_file)


def test_generate_diff_identical_files(sample_files, exp_val_identical_files):
    file_path = sample_files[0]
    expected_value = exp_val_identical_files

    assert generate_diff(file_path, file_path) == expected_value


def test_generate_diff_empty_file(sample_files, exp_val_empty_file):
    file_path1 = sample_files[0]
    file_path2 = sample_files[2]
    expected_value = exp_val_empty_file

    assert generate_diff(file_path1, file_path2) == expected_value


def test_generate_diff_different_files(sample_files, exp_val_different_files):
    file_path1 = sample_files[0]
    file_path2 = sample_files[1]
    expected_value1 = exp_val_different_files[0]
    expected_value2 = exp_val_different_files[1]

    assert generate_diff(file_path1, file_path2) == expected_value1
    assert generate_diff(file_path2, file_path1) == expected_value2
