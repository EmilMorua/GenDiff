from find_diff.convert_bool import convert_dict_values
from find_diff.comparison import DICT1, DICT2, BOTH


def dic_to_string(dic, depth=0, indent=4):
    """Returns a string representation of the given dictionary."""

    result = "{"

    for key, value in dic.items():
        result += "\n" + " " * (indent * (depth + 1)) + str(key) + ": "
        if isinstance(value, dict):
            result += dic_to_string(value, depth + 1, indent)
        else:
            result += str(value)
    result += "\n" + " " * (indent * depth) + "}"

    return result


def get_diff_stylish(diff_dict: dict) -> str:
    """
    Returns a string representation of the difference
    between two dictionariesin the 'stylish' format.
    """

    diff_dict = convert_dict_values(diff_dict)

    def build_diff_string(
            diff_dict: dict, depth: int = 1, indent: int = 4) -> str:
        diff_string = ""

        for key, values in diff_dict.items():
            nested_indent = " " * (indent * depth)

            if isinstance(values, dict) and \
                    not {DICT1, DICT2, BOTH} & set(values):
                nested_diff = build_diff_string(values, depth + 1, indent)
                if nested_diff:
                    diff_string += (
                        f"{nested_indent}{key}: "
                        f"{{\n{nested_diff}{nested_indent}}}\n"
                    )
                continue
            for prefix, dict_key in [("-", DICT1), ("+", DICT2)]:
                if dict_key in values and isinstance(values[dict_key], dict):
                    nested_diff = dic_to_string(
                        values[dict_key], depth, indent
                    )
                    diff_string += (
                        f"{nested_indent[2:]}{prefix} "
                        f"{key}: {nested_diff}\n"
                    )
                elif dict_key in values:
                    diff_string += (
                        f"{nested_indent[2:]}{prefix} "
                        f"{key}: {values[dict_key]}\n"
                    )
            if BOTH in values and isinstance(values[BOTH], dict):
                nested_diff = dic_to_string(values[BOTH], depth, indent)
                if ":" in nested_diff:
                    diff_string += (
                        f"{nested_indent} {key}: {{\n"
                        f"{nested_diff}{nested_indent}}}\n"
                    )
                else:
                    diff_string += f"{nested_indent} {key}: {nested_diff}\n"
            elif BOTH in values:
                diff_string += f"{nested_indent}{key}: {values[BOTH]}\n"

        return diff_string

    return "{\n" + build_diff_string(diff_dict) + "}"
