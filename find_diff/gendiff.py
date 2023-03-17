import json
import itertools


def unpack_json(file_path: str) -> dict:
    with open(file_path) as f:
        content = json.load(f)

    return content


def generate_diff(file_path1: str, file_path2: str) -> str:
    file1, file2 = unpack_json(file_path1), unpack_json(file_path2)
    keys1, keys2 = file1.keys(), file2.keys()
    all_keys = list(set(list(itertools.chain(keys1, keys2))))
    all_keys.sort()

    result = '{\n  '
    for key in all_keys:
        if key in keys1 and key in keys2:
            if file1[key] == file2[key]:
                result += f'  {key}: {file1[key]}\n  '
            else:
                result += f'- {key}: {file1[key]}\n  + {key}: {file2[key]}\n  '
        elif key in keys1:
            result += f'- {key}: {file1[key]}\n  '
        else:
            result += f'+ {key}: {file2[key]}\n  '

    result = result.rstrip() + '\n}'
    return result
