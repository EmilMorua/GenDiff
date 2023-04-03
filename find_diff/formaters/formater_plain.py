from find_diff.convert_bool import convert_dict_values


def get_diff_plain(diff_dict: dict) -> str:
    """
    Returns a string representation of the differences
    between two dictionaries.
    """

    diff_dict = convert_dict_values(diff_dict)

    def process_dict(diff_dict, path=''):
        diff_list = []

        for key, value in diff_dict.items():
            current_path = f'{path}.{key}' if path else key
            if isinstance(value, dict) \
                    and not {'dict1', 'dict2', 'both'} & set(value.keys()):
                sub_diff = process_dict(value, current_path)
                if sub_diff:
                    diff_list.append(sub_diff)
            elif 'dict1' in value and 'dict2' in value:
                if isinstance(value['dict1'], dict) \
                            and isinstance(value['dict2'], dict):
                    sub_diff = process_dict(value['dict1'], current_path)
                    if sub_diff:
                        diff_list.append(sub_diff)
                    sub_diff = process_dict(value['dict2'], current_path)
                    if sub_diff:
                        diff_list.append(sub_diff)
                elif value['dict1'] != value['dict2']:
                    if isinstance(value['dict1'], str) \
                            and isinstance(value['dict2'], str):
                        diff_list.append(
                            f'Property {current_path} was updated. '
                            f"From '{value['dict1']}' to '{value['dict2']}'\n")
                    else:
                        diff_list.append(
                            f'Property {current_path} was updated. '
                            f"From [complex value] to '{value['dict2']}'\n")
            elif 'dict1' in value:
                diff_list.append(f'Property {current_path} was removed\n')
            elif 'dict2' in value:
                if isinstance(value['dict2'], dict):
                    diff_list.append(f"Property {current_path} was "
                                     f"added with value: [complex value]\n")
                else:
                    diff_list.append(f"Property {current_path} was "
                                     f"added with value: '{value['dict2']}'\n")

        return ''.join(diff_list)

    return process_dict(diff_dict)[:-1]
