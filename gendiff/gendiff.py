from gendiff.comparison import compare_dicts
from gendiff.formaters.formater_json import get_diff_json
from gendiff.formaters.formater_plain import get_diff_plain
from gendiff.formaters.formater_stylish import get_diff_stylish
from gendiff.unpack_files import unpack_file


def generate_diff(file_path1: str,
                  file_path2: str,
                  format_name: str = 'stylish') -> str:
    """
    Compare two configuration files and
    return the differences in the specified format.

    Args:
        file_path1: Path to the first configuration file.
        file_path2: Path to the second configuration file.
        format_name: A string representing the output format.
                     Can be 'stylish' (default), 'plain', or 'json'.

    Returns:
        A string representing the differences
        between the two configuration files,
        formatted according to the specified format.

    Raises:
        ValueError: If the specified format is not supported.
    """

    dict1, dict2 = unpack_file(file_path1), unpack_file(file_path2)
    diff_dict = compare_dicts(dict1, dict2)

    if format_name == 'json':
        return get_diff_json(diff_dict)
    elif format_name == 'plain':
        return get_diff_plain(diff_dict)
    elif format_name == 'stylish':
        return get_diff_stylish(diff_dict)
    else:
        raise ValueError
