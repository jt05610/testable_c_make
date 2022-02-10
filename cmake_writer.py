import os
from typing import Union
from templates import get_template
from folder_creation import (
    write,
    touch,
    create_folder,
    find_sub_dir,
    FolderType,
    find_all_directories,
)

# TODO: executables and link libraries


def replace_variables(template_raw: str, **kwargs):
    ret = template_raw
    for key, value in kwargs.items():
        ret = template_raw.replace(f"${key}", value)
    return ret


def write_test_cmake(project_dir: str):
    test_dir = find_sub_dir(project_dir, FolderType.TEST)
    project_name = test_dir.split("/")[-2]
    cmake_file = os.path.join(test_dir, "CMakeLists.txt")
    with open(cmake_file, "w") as f:
        f.write(
            replace_variables(
                get_template(FolderType.TEST), project_name=project_name
            )
        )
    return cmake_file


def get_include_directories(project_dir):
    test_dir = find_sub_dir(project_dir, FolderType.TEST)
    project_name = test_dir.split("/")[-2]
    include_directories = find_all_directories(project_dir, FolderType.INC)
    base_str = "include_directories(${{PROJECT_SOURCE_DIR}}/../{})\n"

    def format_base_str(include_directory: str):
        split = include_directory.split("/")
        proj_index = split.index(project_name) + 1
        return base_str.format("/".join(split[proj_index:]))

    return tuple(map(format_base_str, include_directories))


def lines_in_section(lines, section):
    def guard_index(guard):
        guard_str = f"# {guard} {section}"
        return next(i for i, l in enumerate(lines) if guard_str in l)

    start, end = tuple(map(guard_index, ("begin", "end")))
    return (
        start,
        end,
        tuple(line for line in lines[start + 1 : end] if line != "\n"),
    )


def get_source_files(project_dir):
    test_dir = find_sub_dir(project_dir, FolderType.TEST)
    project_name = test_dir.split("/")[-2]
    source_directories = find_all_directories(project_dir, FolderType.SRC)

    def str_gen():
        base_str = "add_library({} ${{PROJECT_SOURCE_DIR}}/../{})\n"
        for directory in source_directories:
            contents = filter(
                lambda x: x.split(".")[-1] == "c", os.listdir(directory)
            )
            for c in contents:
                path = os.path.join(directory, c)
                split = path.split("/")
                library_name = c.split(".")[0]
                proj_index = split.index(project_name) + 1
                yield base_str.format(
                    library_name, "/".join(split[proj_index:])
                )

    return tuple(str_gen())


def update_cmake_list(project_dir, section: str):
    line_funcs = {
        "libraries": get_source_files,
        "include": get_include_directories,
    }
    test_dir = find_sub_dir(project_dir, FolderType.TEST)
    c_make_list_path = os.path.join(test_dir, "CMakeLists.txt")
    with open(c_make_list_path, "r") as f:
        lines = f.readlines()
    start, end, already_included = lines_in_section(lines, section)
    add_lines = filter(
        lambda x: x not in already_included, line_funcs[section](project_dir)
    )
    for i, line in enumerate(add_lines):
        lines.insert(end + i, line)
    with open(c_make_list_path, "w") as f:
        f.writelines(lines)
    return c_make_list_path
