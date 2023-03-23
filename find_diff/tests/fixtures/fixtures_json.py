import pytest
import os
import json


@pytest.fixture
def sample_data():
    data1 = {"name": "John Doe", "age": 30, "email": "johndoe@example.com"}
    data2 = {"name": "Jane Doe", "age": 50, "phone": "+1-555-555-5555"}
    data3 = {}
    data4 = "invalid json content"
    return data1, data2, data3, data4


@pytest.fixture
def sample_files(tmpdir_factory, sample_data):
    files = []
    for i in range(4):
        filename = f"file{i + 1}.json"
        file_path = tmpdir_factory.mktemp("data").join(filename)
        file_path.write(json.dumps(sample_data[i]))
        files.append(str(file_path))

    yield tuple(files)

    for file_path in files:
        os.remove(file_path)


@pytest.fixture
def non_existent_file_json():
    return "nonexistent_file.json"


@pytest.fixture
def exp_val_dicts_identical():
    return {"name": {"both": "John Doe"},
            "age": {"both": 30},
            "email": {"both": "johndoe@example.com"}
            }


@pytest.fixture
def exp_val_dicts_different():
    return {
            'age': {'dict1': 30, 'dict2': 50},
            'email': {'dict1': 'johndoe@example.com'},
            'name': {'dict1': 'John Doe', 'dict2': 'Jane Doe'},
            'phone': {'dict2': '+1-555-555-5555'}
            }


@pytest.fixture
def exp_val_dicts_empty():
    expected_value1 = {
            'age': {'dict1': 30},
            'email': {'dict1': 'johndoe@example.com'},
            'name': {'dict1': 'John Doe'}
            }
    expected_value2 = {
        'age': {'dict2': 30},
        'email': {'dict2': 'johndoe@example.com'},
        'name': {'dict2': 'John Doe'}
    }

    return expected_value1, expected_value2


@pytest.fixture
def exp_val_identical_files():
    return (
        '{\n'
        '  age: 30\n'
        '  email: johndoe@example.com\n'
        '  name: John Doe\n'
        '}'
    )


@pytest.fixture
def exp_val_empty_file():
    return (
        "{\n"
        "  - age: 30\n"
        "  - email: johndoe@example.com\n"
        "  - name: John Doe\n"
        "}"
    )


@pytest.fixture
def exp_val_different_files():
    expected_value1 = (
        '{\n'
        '  - age: 30\n'
        '  + age: 50\n'
        '  - email: johndoe@example.com\n'
        '  - name: John Doe\n'
        '  + name: Jane Doe\n'
        '  + phone: +1-555-555-5555\n'
        '}'
    )
    expected_value2 = (
        '{\n'
        '  - age: 50\n'
        '  + age: 30\n'
        '  + email: johndoe@example.com\n'
        '  - name: Jane Doe\n'
        '  + name: John Doe\n'
        '  - phone: +1-555-555-5555\n'
        '}'
    )

    return expected_value1, expected_value2
