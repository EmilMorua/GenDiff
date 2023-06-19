import json
from gendiff.comparison import KEY, TYPE, VALUE, CHILDREN
from gendiff.comparison import BEFORE_VALUE, AFTER_VALUE, DICT1, DICT2, BOTH


def get_diff_json(diff_dict):
    """
    Recursively generates a list of differences
    between two dictionaries in JSON format.
    """

    result = []
    for key, value in diff_dict.items():
        if isinstance(value, dict) and \
                not {DICT1, DICT2, BOTH} & set(value.keys()):
            result.append({
                KEY: key,
                TYPE: 'hasChildren',
                CHILDREN: get_diff_json(value)
            })
        elif DICT1 in value and DICT2 in value:
            before_value = value[DICT1]
            after_value = value[DICT2]
            if isinstance(before_value, str) and \
                    before_value.lower() in ['true', 'false', 'null']:
                before_value = json.loads(before_value.lower())
            if isinstance(after_value, str) and \
                    after_value.lower() in ['true', 'false', 'null']:
                after_value = json.loads(after_value.lower())
            result.append({
                KEY: key,
                TYPE: 'changed',
                BEFORE_VALUE: before_value,
                AFTER_VALUE: after_value
            })
        elif DICT1 in value:
            result.append({
                KEY: key,
                TYPE: 'deleted',
                VALUE: value[DICT1]
            })
        elif DICT2 in value:
            result.append({
                KEY: key,
                TYPE: 'added',
                VALUE: value[DICT2]
            })
        elif BOTH in value:
            result.append({
                KEY: key,
                TYPE: 'unchanged',
                VALUE: value[BOTH]
            })

    return result
