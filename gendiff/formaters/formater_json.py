import json
from gendiff.comparison import KEY, TYPE, VALUE, CHILDREN
from gendiff.comparison import BEFORE_VALUE, AFTER_VALUE, DICT1, DICT2, BOTH


def get_diff_json(diff_dict):
    """
    Recursively generates a list of differences
    between two dictionaries in JSON format.
    """
    def get_diff(diff_dict):
        result = []
        for key, value in diff_dict.items():
            if isinstance(value, dict) and \
                    not {DICT1, DICT2, BOTH} & set(value.keys()):
                result.append({
                    KEY: key,
                    TYPE: "hasChildren",
                    CHILDREN: get_diff(value)
                })
            elif DICT1 in value and DICT2 in value:
                before_value = value[DICT1]
                after_value = value[DICT2]
                result.append({
                    KEY: key,
                    TYPE: "changed",
                    BEFORE_VALUE: before_value,
                    AFTER_VALUE: after_value
                })
            elif DICT1 in value:
                result.append({
                    KEY: key,
                    TYPE: "deleted",
                    VALUE: value[DICT1]
                })
            elif DICT2 in value:
                result.append({
                    KEY: key,
                    TYPE: "added",
                    VALUE: value[DICT2]
                })
            elif BOTH in value:
                result.append({
                    KEY: key,
                    TYPE: "unchanged",
                    VALUE: value[BOTH]
                })

        return result

    def convert_to_string(diff_dict):
        result = json.dumps(diff_dict, ensure_ascii=False, indent=None)
        result = result.replace("\\", "")
        return result

    result = get_diff(diff_dict)
    result = convert_to_string(result)

    return result
