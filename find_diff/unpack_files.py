import json
import os
import yaml


def get_file_format(path: str) -> str:
    """Get the file format of the specified file."""

    _, ext = os.path.splitext(path)
    if ext == '.json':
        return 'json'
    elif ext in ('.yaml', '.yml'):
        return 'yaml'
    else:
        raise ValueError(f"Unrecognized file format for file {path}")


def unpack_file(file_path: str) -> dict:
    """Read and parse the content of a file in JSON or YAML format."""

    with open(file_path) as file:
        try:
            format = get_file_format(file_path)
            if format == 'json':
                content = json.load(file, parse_constant=lambda x: x)
            elif format == 'yaml':
                content = yaml.safe_load(file)
        except FileNotFoundError:
            raise FileNotFoundError(f"{file_path} does not exist")
        except (json.JSONDecodeError, yaml.YAMLError):
            raise ValueError(f"{file_path} is not a valid file format")

        return content
