import unittest
import os
import shutil

import folder_creation
import cmake_writer


class CMakeWriteTest(unittest.TestCase):
    def setUp(self) -> None:
        self.project_name = "test_project"
        self.test_dir = os.path.join(os.getcwd(), "tmp")
        try:
            os.mkdir(self.test_dir)
        except FileExistsError:
            shutil.rmtree(self.test_dir)
            os.mkdir(self.test_dir)
        self.project_dir = folder_creation.create_project_structure(
            self.project_name, self.test_dir
        )

    def tearDown(self) -> None:
        pass

    def test_write_main_project_cmake(self):
        expected = cmake_writer.get_template("Test").replace(
            "$project_name", self.project_name
        )
        result_file = cmake_writer.write_test_cmake(self.project_dir)
        with open(result_file, "r") as f:
            actual_contents = f.read()
        self.assertEqual(expected, actual_contents)

    def test_get_include_directories(self):
        folder_creation.add_driver_structure("test_driver")
        directories = cmake_writer.get_include_directories(self.project_dir)
        print(directories)
        self.assertEqual(4, len(directories))

    def test_update_include_directories(self):
        path = cmake_writer.write_test_cmake(self.project_dir)
        with open(path, "r") as f:
            old = f.readlines()
        cmake_writer.update_cmake_list(self.project_dir, "include")
        with open(path, "r") as f:
            new = f.readlines()
        self.assertEqual(3, len(new) - len(old))

    def test_get_source_files(self):
        driver_dir = folder_creation.add_driver_structure("test_driver")
        driver_src = folder_creation.find_sub_dir(driver_dir, "Src")
        folder_creation.touch(driver_src, "test_driver.c")
        self.assertEqual(
            1, len(cmake_writer.get_source_files(self.project_dir))
        )

    def test_update_source_files(self):
        path = cmake_writer.write_test_cmake(self.project_dir)
        driver_dir = folder_creation.add_driver_structure("test_driver")
        driver_src = folder_creation.find_sub_dir(driver_dir, "Src")
        folder_creation.touch(driver_src, "test_driver.c")
        with open(path, "r") as f:
            old = f.readlines()
        cmake_writer.update_cmake_list(self.project_dir, "libraries")
        with open(path, "r") as f:
            new = f.readlines()
        self.assertEqual(1, len(new) - len(old))
