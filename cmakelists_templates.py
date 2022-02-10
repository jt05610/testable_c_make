def get_main_template(project_name: str, cmake_version: str = "3.21"):
    return (
        f"cmake_minimum_required(VERSION {cmake_version})\n"
        f"project({project_name})\n"
        f"\n"
        f"set(CMAKE_C_STANDARD 99)\n"
        f"\n"
        f"if (DEFINED ENV{{CPPUTEST_HOME}})\n"
        f"    message('Using CppUTest found in $ENV{{CPPUTEST_HOME}}')\n"
        f"else ()\n"
        f"    message('CPPUTEST_HOME is not set; You must tell CMake where to find CppUTest')\n"
        f"    return ()\n"
        f"endif()\n"
        f"\n"
        f"enable_language(C)\n"
        f"enable_language(CXX)\n"
        f"\n"
        f"# The version number\n"
        f"set({project_name}_VERSION_MAJOR 1)\n"
        f"set({project_name}_VERSION_MINOR 0)\n"
        f"\n"
        f"set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${{PROJECT_BINARY_DIR}}/bin)\n"
        f"set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${{PROJECT_BINARY_DIR}}/lib)\n"
        f"set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${{PROJECT_BINARY_DIR}}/lib)\n"
        f"\n"
        f"add_subdirectory(src)\n"
        f"add_subdirectory(mocks)\n"
        f"add_subdirectory(tests)"
    )


def get_mocks_template(project_name: str):
    return (
        f"project ({project_name})\n"
        f"\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../include)\n"
        f"add_library(mockLib mockLib.c)"
    )


def get_src_template(project_name: str):
    return (
        f"project ({project_name})\n"
        f"\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../include)\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../include/{project_name}/)\n"
        f"# uncomment below and make changes as necessary to add library to project\n"
        f"# include_directories(${{PROJECT_SOURCE_DIR}}/../include/ExtraLibrary/)\n"
        f"\n"
        f"configure_file (\n"
        f'    "${{PROJECT_SOURCE_DIR}}/../include/{project_name}Config.h.in"\n'
        f'    "${{PROJECT_BINARY_DIR}}/{project_name}Config.h"\n'
        f")\n"
        f"# uncomment below and make changes as necessary to add library to project\n"
        f"# add_library(ExtraLibrary ./ExtraLibrary.c)\n"
        f"\n"
        f"add_library({project_name} ./{project_name}/{project_name}.c)\n"
        f"add_executable(main ./main.c)\n"
        f"target_link_libraries(main {project_name})"
    )


def get_tests_template(project_name: str, cmake_version: str = "3.21"):
    return (
        f"project({project_name})\n"
        f"cmake_minimum_required(VERSION {cmake_version})\n"
        f"\n"
        f"# include project source\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../include)\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../include/{project_name})\n"
        f"\n"
        f"# include mocks only for test code\n"
        f"include_directories(${{PROJECT_SOURCE_DIR}}/../mocks)\n"
        f"\n"
        f"# include CppUTest headers\n"
        f"include_directories($ENV{{CPPUTEST_HOME}}/include)\n"
        f"\n"
        f"# add cpputest library\n"
        f"add_library(imp_cpputest STATIC IMPORTED)\n"
        f"set_property(TARGET imp_cpputest PROPERTY\n"
        f"IMPORTED_LOCATION $ENV{{CPPUTEST_HOME}}/cpputest_build/lib/libCppUTest.a)\n"
        f"\n"
        f"add_library({project_name}Test ./{project_name}/{project_name}Test.cpp)\n"
        f"add_executable(RunAllTests RunAllTests.cpp)\n"
        f"target_link_libraries(RunAllTests imp_cpputest {project_name}Test {project_name})"
    )
