from gendiff.comparison import KEY, TYPE, VALUE, CHILDREN
from gendiff.comparison import BEFORE_VALUE, AFTER_VALUE, DICT1, DICT2, BOTH


def get_diff_json(diff_dict):
    """
    Recursively generates a list of differences
    between two dictionaries in JSON format.
    """

    result = []
    for key, value in diff_dict.items():
        if isinstance(value, dict) and not {DICT1, DICT2, BOTH} & set(value.keys()):
            result.append({
                KEY: key,
                TYPE: 'hasChildren',
                CHILDREN: get_diff_json(value)
            })
        elif DICT1 in value and DICT2 in value:
            if isinstance(value[DICT1], dict) or isinstance(value[DICT2], dict):
                result.append({
                    KEY: key,
                    TYPE: 'hasChildren',
                    CHILDREN: get_diff_json({DICT1: value[DICT1], DICT2: value[DICT2]})
                })
            elif value[DICT1] != value[DICT2]:
                result.append({
                    KEY: key,
                    TYPE: 'changed',
                    BEFORE_VALUE: value[DICT1],
                    AFTER_VALUE: value[DICT2]
                })
            else:
                result.append({
                    KEY: key,
                    TYPE: 'unchanged',
                    VALUE: value[DICT1]
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
