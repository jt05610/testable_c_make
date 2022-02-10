import os
import argparse
from folder_creation import write
from source_templates import get_main_test, get_library_main
from header_templates import get_header


def create_test_file(test_name: str):
    # create test.cpp file with TEST_GROUP and failing TEST
    parent = os.getcwd()
    path = os.path.join(parent, f"{test_name}Test.cpp")
    write(path, get_main_test(test_name))


def get_test_folder(parent_dir):
    split_parent = parent_dir.split("/")
    test_i = -1
    for i, name in enumerate(split_parent):
        if name == "tests":
            test_i = i
    test_path_split = split_parent[: test_i + 1]
    return os.path.join("/", *test_path_split)


def get_last_line_of_group(lines: list, search_text: str):
    ret = 0
    for line_i, line in enumerate(lines):
        if line.split("(")[0] == search_text:
            ret = line_i
    return ret


def update_link_libraries(lines, library):
    link_line = get_last_line_of_group(lines, "target_link_libraries")
    new_link_line = lines[link_line].strip(")") + f" {library})"
    lines[link_line] = new_link_line
    return lines


def add_library_to_cmakelists(lines: list, test_name: str):
    max_add_library = get_last_line_of_group(lines, "add_library")
    new_line = f'add_library({test_name} ./{os.getcwd().split("/")[-1]}/{test_name}.c)\n'
    lines.insert(max_add_library + 1, new_line)
    return lines


def get_cmakelist_updater(testing_lib: bool = False):
    def update_cmakelists(test_name: str):
        # add test to tests/CMakeLists.txt
        test_path = get_test_folder(os.getcwd())
        cmake_path = os.path.join(test_path, "CMakeLists.txt")
        with open(cmake_path, "r") as f:
            lines = f.readlines()
        # link test to RunAllTests
        lines = update_link_libraries(lines, f"{test_name}Test")
        lines = update_link_libraries(lines, f"{test_name}")
        if testing_lib:
            lines = add_library_to_cmakelists(lines, f"{test_name}")
        max_add_library = get_last_line_of_group(lines, "add_library")
        new_line = f'add_library({test_name}Test ./{os.getcwd().split("/")[-1]}/{test_name}Test.cpp)\n'
        lines.insert(max_add_library + 1, new_line)

        with open(cmake_path, "w") as f:
            f.writelines(lines)

    return update_cmakelists


def update_test_runner(test_name: str):
    # add IMPORT_TEST_GROUP statement to RunAllTests
    test_path = get_test_folder(os.getcwd())
    test_runner = os.path.join(test_path, "RunAllTests.cpp")
    with open(test_runner, "r") as f:
        lines = f.readlines()

    test_import_line = get_last_line_of_group(lines, "IMPORT_TEST_GROUP")
    new_line = f"IMPORT_TEST_GROUP({test_name});\n"
    lines.insert(test_import_line + 1, new_line)

    with open(test_runner, "w") as f:
        f.writelines(lines)


def create_test_header(test_name: str):
    parent = os.getcwd()
    path = os.path.join(parent, f"{test_name}.h")
    project_name = parent.split("/")[-1]
    write(path, get_header(project_name, test_name))


def create_test_source(test_name: str):
    parent = os.getcwd()
    path = os.path.join(parent, f"{test_name}.c")
    write(path, get_library_main(test_name))


def add_test(test_name: str):
    for task in (
        create_test_file,
        get_cmakelist_updater(True),
        update_test_runner,
        create_test_header,
        create_test_source,
    ):
        task(test_name)


def main():
    parser = argparse.ArgumentParser(
        description="Create library for testing and a test for that library in the current folder.\n"
        "Must be run from <project_name>/tests/<project_name>\n"
    )
    parser.add_argument("name", type=str, help="the name of the test library")
    test_library_name = parser.parse_args().name
    add_test(test_library_name)
    print(f"Successfully created {test_library_name}.")
