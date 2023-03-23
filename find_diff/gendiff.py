import json
import itertools
import io
from typing import Any


def unpack_json(file_path: str) -> dict:
    """
    Loads and returns the JSON content from the file at the given file path.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict:
            A dictionary representing the JSON content of the file.

    Raises:
        ValueError:
                  If the file at the given file path is not a valid JSON file.
    """

    with open(file_path) as f:
        try:
            with open(file_path) as f:
                content = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"{file_path} does not exist")
        except json.JSONDecodeError:
            raise ValueError(f"{file_path} is not a valid JSON file")

        return content


def compare_dicts(dict1: dict, dict2: dict) -> dict[str, dict[str, Any]]:
    """
    Compares two dictionaries and returns a dictionary of the differences.

    Args:
        dict1 (dict): The first dictionary to compare.
        dict2 (dict): The second dictionary to compare.

    Returns:
        dict:
            A dictionary of the differences between the two input dictionaries.
            The keys are the keys that are present in either dictionary, and
            the values are themselves dictionaries containing the differences.
    """

    keys1, keys2 = set(dict1.keys()), set(dict2.keys())
    all_keys = list(set(itertools.chain(keys1, keys2)))
    all_keys = sorted(all_keys, key=lambda x: x.lower())

    diff_dict = {}
    for key in all_keys:
        if key in keys1 and key in keys2:
            if dict1[key] != dict2[key]:
                diff_dict[key] = {'dict1': dict1[key], 'dict2': dict2[key]}
            else:
                diff_dict[key] = {'both': dict1[key]}
        elif key in keys1:
            diff_dict[key] = {'dict1': dict1[key]}
        else:
            diff_dict[key] = {'dict2': dict2[key]}

    return diff_dict


def generate_diff(file_path1: str, file_path2: str) -> str:
    """
    Generates a diff string between two JSON files.

    Args:
        file_path1 (str): The path to the first JSON file to be compared.
        file_path2 (str): The path to the second JSON file to be compared.

    Returns:
        str: A string containing the differences between the two input files.

    """

    dict1, dict2 = unpack_json(file_path1), unpack_json(file_path2)
    diff_dict = compare_dicts(dict1, dict2)

    with io.StringIO() as result:
        result.write('{\n')
        for key, values in diff_dict.items():
            if 'dict1' in values and 'dict2' in values:
                result.write(f'  - {key}: {values["dict1"]}\n'
                             f'  + {key}: {values["dict2"]}\n'
                             )
            elif 'dict1' in values:
                result.write(f'  - {key}: {values["dict1"]}\n')
            elif 'dict2' in values:
                result.write(f'  + {key}: {values["dict2"]}\n')
            else:
                result.write(f'  {key}: {values["both"]}\n')

        result.write('}')
        return result.getvalue()


#path = '/Users/chibis/code/Projects/Project_2/python-project-50/find_diff/tests/file_examples/file4.json'
#print(unpack_json(path))