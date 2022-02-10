import unittest
import os
import shutil
import folder_creation


class FolderCreationTest(unittest.TestCase):
    def setUp(self) -> None:
        self.test_dir = os.path.join(os.getcwd(), "tmp")
        try:
            os.mkdir(self.test_dir)
        except FileExistsError:
            shutil.rmtree(self.test_dir)
            os.mkdir(self.test_dir)

    def tearDown(self) -> None:
        os.chdir(folder_creation.get_parent_dir(self.test_dir))

    def expect_read(self, name, contents):
        path = os.path.join(self.test_dir, name)
        with open(path, "r") as f:
            actual = f.read()
        self.assertEqual(contents, actual)

    def test_create_folder_already_exists_no_overwrite(self):
        folder = folder_creation.create_folder(self.test_dir, "test_parent")
        folder_creation.touch(folder, "keep_me")
        folder_creation.create_folder(self.test_dir, "test_parent")
        self.assertEqual(1, len(os.listdir(folder)))

    def test_create_folder_already_exists_overwrite(self):
        folder = folder_creation.create_folder(self.test_dir, "test_parent")
        folder_creation.touch(folder, "keep_me")
        folder_creation.create_folder(
            self.test_dir, "test_parent", overwrite=True
        )
        self.assertEqual(0, len(os.listdir(folder)))

    def test_touch(self):
        folder_creation.touch(self.test_dir, "test.txt")
        self.assertEqual(1, len(os.listdir(self.test_dir)))

    def test_write(self):
        folder_creation.write(self.test_dir, "test.txt", "test")
        self.assertEqual(1, len(os.listdir(self.test_dir)))
        self.expect_read("test.txt", "test")

    def test_create_folder(self):
        folder_creation.create_folder(self.test_dir, "test_parent")
        self.assertEqual(1, len(os.listdir(self.test_dir)))

    def test_create_base_folder_structure(self):
        project_dir = folder_creation.create_project_structure(
            "test_project", self.test_dir
        )
        self.assertEqual(4, len(os.listdir(project_dir)))

    def test_create_base_folder_structure_from_temp_folder(self):
        os.chdir(self.test_dir)
        project_dir = folder_creation.create_project_structure(
            "test_project",
        )
        self.assertTrue(self.test_dir in project_dir)
        self.assertEqual(4, len(os.listdir(project_dir)))

    def test_add_driver(self):
        project_dir = folder_creation.create_project_structure(
            "test_project", self.test_dir
        )
        folder_creation.add_driver_structure("test_driver")
        self.assertEqual(
            1, len(os.listdir(os.path.join(project_dir, "Drivers")))
        )
        self.assertEqual(
            2,
            len(
                os.listdir(os.path.join(project_dir, "Drivers", "test_driver"))
            ),
        )

    def test_add_driver_from_different_folder(self):
        project_dir = folder_creation.create_project_structure(
            "test_project", self.test_dir
        )
        os.chdir(os.path.join(project_dir, "Core", "Src"))
        folder_creation.add_driver_structure("test_driver")
        self.assertEqual(
            1, len(os.listdir(os.path.join(project_dir, "Drivers")))
        )
        self.assertEqual(
            2,
            len(
                os.listdir(os.path.join(project_dir, "Drivers", "test_driver"))
            ),
        )

    def test_find_all_directories(self):
        project_dir = folder_creation.create_project_structure(
            "test_project", self.test_dir
        )
        folder_creation.add_driver_structure("test_driver")
        result = folder_creation.find_all_directories(project_dir, "Inc")
        self.assertEqual(4, len(result))

    def test_find_sub_dir_when_called_from_that_dir(self):
        project_dir = folder_creation.create_project_structure(
            "test_project", self.test_dir
        )
        test_dir = os.path.join(project_dir, "Test")
        res = folder_creation.find_sub_dir(test_dir, "Test")
        self.assertEqual(test_dir, res)

    def test_folder_type_str(self):
        self.assertEqual("Core", str(folder_creation.FolderType.CORE))

    def test_find_sub_dir_raises_exception_when_too_deep(self):
        folder = folder_creation.create_folder(self.test_dir, str(0))
        for i in range(1, 10):
            folder = folder_creation.create_folder(folder, str(i))
        with self.assertRaises(folder_creation.TooDeepError):
            _ = folder_creation.find_sub_dir(folder, "0")
