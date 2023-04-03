def convert_dict_values(input_dict):
    if not isinstance(input_dict, dict):
        return input_dict

    output_dict = {}
    for key, value in input_dict.items():
        if isinstance(value, dict):
            output_dict[key] = convert_dict_values(value)
        elif value is None:
            output_dict[key] = 'null'
        elif value is True:
            output_dict[key] = 'true'
        elif value is False:
            output_dict[key] = 'false'
        else:
            output_dict[key] = value

    return output_dict
