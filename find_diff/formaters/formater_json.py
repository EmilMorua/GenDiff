def get_diff_json(diff_dict):
    """
    Recursively generates a list of differences
    between two dictionaries in JSON format.
    """

    result = []
    for key, value in diff_dict.items():
        if isinstance(value, dict) \
                and not {'dict1', 'dict2', 'both'} & set(value.keys()):
            result.append({
                'key': key,
                'type': 'hasChildren',
                'children': get_diff_json(value)
            })
        elif 'dict1' in value and 'dict2' in value:
            result.append({
                'key': key,
                'type': 'changed',
                'beforeValue': value['dict1'],
                'afterValue': value['dict2']
            })
        elif 'dict1' in value:
            result.append({
                'key': key,
                'type': 'deleted',
                'value': value['dict1']
            })
        elif 'dict2' in value:
            result.append({
                'key': key,
                'type': 'added',
                'value': value['dict2']
            })
        elif 'both' in value:
            result.append({
                'key': key,
                'type': 'unchanged',
                'value': value['both']
            })

    return result
