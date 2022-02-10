import os
from folder_creation import get_parent_dir


def get_template(folder_type: str):
    parent_dir = get_parent_dir(__file__)
    with open(
        os.path.join(parent_dir, f"{folder_type}_CMakeLists.txt.template"), "r"
    ) as f:
        template = f.read()
    return template
