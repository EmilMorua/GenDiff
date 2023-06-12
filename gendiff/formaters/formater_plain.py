from gendiff.convert_bool import convert_dict_values
from gendiff.comparison import DICT1, DICT2, BOTH


def wrap_values_in_quotes(diff_dict):
    for key, value in diff_dict.items():
        if isinstance(value, dict):
            wrap_values_in_quotes(value)
        elif isinstance(value, str) and value.lower() in ['true', 'false']:
            diff_dict[key] = value.lower()
        elif not isinstance(value, str) and not isinstance(value, int):
            diff_dict[key] = f"'{value}'"
    return diff_dict


def get_diff_plain(diff_dict: dict) -> str:
    """
    Returns a string representation of the differences
    between two dictionaries.
    """
    diff_dict = convert_dict_values(diff_dict)
    diff_dict = wrap_values_in_quotes(diff_dict)
    diff_list = []
    process_dict(diff_dict, diff_list)
    return ''.join(diff_list)[:-1]


def process_dict(diff_dict, diff_list, path=''):
    for key, value in diff_dict.items():
        current_path = f'{path}.{key}' if path else key
        if isinstance(value, dict) and not {DICT1, DICT2, BOTH} \
                & set(value.keys()):
            process_dict(value, diff_list, current_path)
        elif DICT1 in value and DICT2 in value:
            process_updated_value(value, diff_list, current_path)
        elif DICT1 in value:
            process_removed_value(diff_list, current_path)
        elif DICT2 in value:
            process_added_value(value, diff_list, current_path)


def process_updated_value(value, diff_list, current_path):
    dict1_value = value[DICT1]
    dict2_value = value[DICT2]

    if isinstance(dict1_value, str) and \
            dict1_value.lower() not in ['true', 'false', 'null']:
        dict1_value = f"'{dict1_value}'"
    elif isinstance(dict1_value, dict):
        dict1_value = "[complex value]"
    elif isinstance(dict1_value, int):
        dict1_value = f"{dict1_value}"

    if isinstance(dict2_value, str) and \
            dict2_value.lower() not in ['true', 'false', 'null']:
        dict2_value = f"'{dict2_value}'"
    elif isinstance(dict2_value, dict):
        dict2_value = "[complex value]"
    elif isinstance(dict2_value, int):
        dict2_value = f"{dict2_value}"

    update_text = f"From {dict1_value} to {dict2_value}"
    diff_list.append(
        f"Property '{current_path}' "
        f"was updated. {update_text}\n")


def process_removed_value(diff_list, current_path):
    diff_list.append(f"Property '{current_path}' was removed\n")


def process_added_value(value, diff_list, current_path):
    dict2_value = value[DICT2]
    if isinstance(dict2_value, dict):
        diff_list.append(
            f"Property '{current_path}' was "
            f"added with value: [complex value]\n")
    else:
        if isinstance(dict2_value, str) and \
                dict2_value.lower() not in ['true', 'false', 'null']:
            dict2_value = f"'{dict2_value}'"
        elif isinstance(dict2_value, dict):
            dict2_value = "[complex value]"
        diff_list.append(
            f"Property '{current_path}' was "
            f"added with value: {dict2_value}\n")


diff_dict = {"common": {"follow": {"dict2": "false"}, "setting1": {"both": "Value 1"}, "setting2": {"dict1": 200}, "setting3": {"dict1": "true", "dict2": "null"}, "setting4": {"dict2": "blah blah"}, "setting5": {"dict2": {"key5": "value5"}}, "setting6": {"doge": {"wow": {"dict1": "", "dict2": "so much"}}, "key": {"both": "value"}, "ops": {"dict2": "vops"}}}, "group1": {"baz": {"dict1": "bas", "dict2": "bars"}, "foo": {"both": "bar"}, "nest": {"dict1": {"key": "value"}, "dict2": "str"}}, "group2": {"dict1": {"abc": 12345, "deep": {"id": 45}}}, "group3": {"dict2": {"deep": {"id": {"number": 45}}, "fee": 100500}}}

print(get_diff_plain(diff_dict))