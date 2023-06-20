from typing import Any


KEY = "key"
TYPE = "type"
VALUE = "value"
CHILDREN = "children"
BEFORE_VALUE = "beforeValue"
AFTER_VALUE = "afterValue"
DICT1 = "dict1"
DICT2 = "dict2"
BOTH = "both"


def compare_dicts(dict1: dict, dict2: dict) -> dict[str, dict[str, Any]]:
    """Compares two dictionaries and returns a dictionary of differences.

    Args:
        dict1: A dictionary to compare.
        dict2: A dictionary to compare.

    Returns:
        A dictionary of differences between `dict1` and `dict2`,
        where the keys are the common keys in both dictionaries,
        and the values are either nested dictionaries of differences
        or dictionaries with the keys 'dict1', 'dict2', or 'both'
        and their corresponding values from `dict1` and `dict2`.
    """

    keys1, keys2 = set(dict1.keys()), set(dict2.keys())
    all_keys = sorted(keys1 | keys2, key=str.lower)

    diff_dict = {}
    for key in all_keys:
        if key not in keys1:
            diff_dict[key] = {DICT2: dict2[key]}
            continue
        if key not in keys2:
            diff_dict[key] = {DICT1: dict1[key]}
            continue
        if isinstance(dict1[key], dict) and isinstance(dict2[key], dict):
            nested_diff = compare_dicts(dict1[key], dict2[key])
            if nested_diff:
                diff_dict[key] = nested_diff
                continue
        if dict1[key] != dict2[key]:
            diff_dict[key] = {DICT1: dict1[key], DICT2: dict2[key]}
        else:
            diff_dict[key] = {BOTH: dict1[key]}

    return diff_dict
