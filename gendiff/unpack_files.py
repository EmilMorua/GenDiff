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


def read_file(file_path: str) -> str:
    """Read the content of a file."""
    with open(file_path) as file:
        content = file.read()
    return content


def parse_content(content: str, format: str) -> dict:
    """Parse the content of a file in JSON or YAML format."""
    if format == 'json':
        try:
            parsed_content = json.loads(content)
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format")
    elif format == 'yaml':
        try:
            parsed_content = yaml.safe_load(content)
        except yaml.YAMLError:
            raise ValueError("Invalid YAML format")
    else:
        raise ValueError("Invalid file format")

    return parsed_content


def unpack_file(file_path: str) -> dict:
    """Read and parse the content of a file in JSON or YAML format."""
    try:
        file_format = get_file_format(file_path)
        file_content = read_file(file_path)
        parsed_content = parse_content(file_content, file_format)
    except FileNotFoundError:
        raise FileNotFoundError(f"{file_path} does not exist")

    return parsed_content
