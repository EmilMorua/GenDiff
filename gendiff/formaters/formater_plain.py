from gendiff.convert_bool import convert_dict_values
from gendiff.comparison import DICT1, DICT2, BOTH


def wrap_values_in_quotes(diff_dict):
    for key, value in diff_dict.items():
        if isinstance(value, dict):
            wrap_values_in_quotes(value)
        elif isinstance(value, str) and value.lower() in ['true', 'false']:
            diff_dict[key] = value.lower()
    return diff_dict


def get_diff_plain(diff_dict: dict) -> str:
    """
    Returns a string representation of the differences
    between two dictionaries.
    """
    diff_dict = convert_dict_values(diff_dict)
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
    if isinstance(dict1_value, str) and isinstance(dict2_value, str):
        update_text = (f"From {dict1_value} to {dict2_value}")
    else:
        update_text = (f"From [complex value] to {dict2_value}")
    diff_list.append(f"Property '{current_path}' "
                     f"was updated. {update_text}\n")


def process_removed_value(diff_list, current_path):
    diff_list.append(f"Property '{current_path}' was removed\n")


def process_added_value(value, diff_list, current_path):
    dict2_value = value[DICT2]
    if isinstance(dict2_value, dict):
        diff_list.append(
            f"Property '{current_path}' was added "
            f"with value: [complex value]\n")
    else:
        diff_list.append(
            f"Property '{current_path}' was added "
            f"with value: '{dict2_value}'\n")
