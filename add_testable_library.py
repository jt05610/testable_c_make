import os
import argparse

from add_test import create_test_file
from source_templates import get_library_main, get_main_test
from header_templates import get_header
from add_test import (
    get_last_line_of_group,
    update_link_libraries,
    create_test_file,
    get_cmakelist_updater,
    update_test_runner,
)
from folder_creation import write


def get_src_folder(parent_dir):
    split_parent = parent_dir.split("/")
    test_i = -1
    for i, name in enumerate(split_parent):
        if name == "src":
            test_i = i
    test_path_split = split_parent[: test_i + 1]
    return os.path.join("/", *test_path_split)


def get_header_folder(parent_dir):
    split_parent = parent_dir.split("/")
    project_name = split_parent[-1]
    test_i = -1
    for i, name in enumerate(split_parent):
        if name == "src":
            test_i = i
    test_path_split = split_parent[:test_i]
    return os.path.join("/", *test_path_split, "include", project_name)


def get_test_folder(parent_dir):
    split_parent = parent_dir.split("/")
    project_name = split_parent[-1]
    test_i = -1
    for i, name in enumerate(split_parent):
        if name == "src":
            test_i = i
    test_path_split = split_parent[:test_i]
    return os.path.join("/", *test_path_split, "tests", project_name)


def add_library_source(library_name):
    # add source file
    parent = os.getcwd()
    path = os.path.join(parent, f"{library_name}.c")
    write(path, get_library_main(library_name))


def update_src_cmakelists(library_name):
    # add source to cmakelists
    # TODO: dont update link libraries if not found
    # TODO: add include directories if not there

    src_path = get_src_folder(os.getcwd())
    cmake_path = os.path.join(src_path, "CMakeLists.txt")
    with open(cmake_path, "r") as f:
        lines = f.readlines()
    lines = update_link_libraries(lines, library_name)

    library_line = get_last_line_of_group(lines, "add_library")
    new_line = f'add_library({library_name} ./{os.getcwd().split("/")[-1]}/{library_name}.c)\n'
    lines.insert(library_line + 1, new_line)

    with open(cmake_path, "w") as f:
        f.writelines(lines)


def add_header(library_name):
    # add header file
    parent = os.getcwd()
    project_name = parent.split("/")[-1]
    header_folder = get_header_folder(parent)
    path = os.path.join(header_folder, f"{library_name}.h")
    write(path, get_header(project_name, library_name))


def add_test_for_library(library_name):
    # add test
    os.chdir(get_test_folder(os.getcwd()))
    create_test_file(library_name)
    get_cmakelist_updater()(library_name)
    update_test_runner(library_name)


def create_library(library_name):
    for task in (
        add_library_source,
        update_src_cmakelists,
        add_header,
        add_test_for_library,
    ):
        task(library_name)


def main():
    parser = argparse.ArgumentParser(
        description="Create library and associated tests.\n"
        "Must be run from <project_name>/src/<project_name>"
    )
    parser.add_argument("name", type=str, help="the name of the library")
    library_name = parser.parse_args().name
    create_library(library_name)
    print(f"Successfully created {library_name}.")
