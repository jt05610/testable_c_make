def get_main(project_name: str):
    return (
        f'#include "{project_name}.h"\n'
        f"\n"
        f"int main (int argc, char ** argv)\n"
        f"{{\n"
        f"    return 0;\n"
        f"}}"
    )


def get_library_main(project_name: str):
    return f'#include "{project_name}.h"\n'


def get_test_runner(project_name: str):
    return (
        f'#include "CppUTest/CommandLineTestRunner.h"\n'
        f"\n"
        f"IMPORT_TEST_GROUP({project_name});\n"
        f"\n"
        f"int main(int argc, char** argv)\n"
        f"{{\n"
        f"    return RUN_ALL_TESTS(argc, argv);\n"
        f"}}"
    )


def get_main_test(project_name: str):
    return (
        f"#pragma clang diagnostic push\n"
        f'#pragma clang diagnostic ignored "-Wunknown-pragmas"\n'
        f'#pragma ide diagnostic ignored "cert-err58-cpp"\n'
        f'#include "CppUTest/TestHarness.h"\n'
        f"\n"
        f'extern "C"\n'
        f"{{\n"
        f'#   include "{project_name}.h"\n'
        f"}}\n"
        f"\n"
        f"TEST_GROUP({project_name})\n"
        f"{{\n"
        f"    void setup()\n"
        f"    {{\n"
        f"\n"
        f"    }}\n"
        f"    void teardown()\n"
        f"    {{\n"
        f"\n"
        f"    }}\n"
        f"}};\n"
        f"\n"
        f"TEST({project_name}, Fails)\n"
        f"{{\n"
        f'    FAIL("If this fails then everything is set up properly.");\n'
        f"}}\n"
        f"\n"
        f"#pragma clang diagnostic pop\n"
    )
