import os
import shutil
from enum import Enum


class FolderType(str, Enum):
    CORE = "Core"
    DRIVERS = "Drivers"
    MOCKS = "Mocks"
    INC = "Inc"
    SRC = "Src"
    TEST = "Test"
    RUNNERS = "Runners"

    def __str__(self):
        return str.__str__(self)


def touch(parent_dir: str, file: str) -> str:
    path = os.path.join(parent_dir, file)
    with open(path, "w") as _:
        pass
    return path


def write(parent_dir: str, file: str, contents: str) -> str:
    path = os.path.join(parent_dir, file)
    with open(path, "w") as f:
        f.write(contents)
    return path


def create_folder(
    parent: str, folder_name: str, overwrite: bool = False
) -> str:
    creating_dir = os.path.join(parent, folder_name)
    try:
        os.mkdir(creating_dir)
    except FileExistsError:
        if overwrite:
            shutil.rmtree(creating_dir)
            create_folder(parent, folder_name)
        else:
            pass
    return creating_dir


def create_project_structure(
    project_name: str, parent_dir: str = None, overwrite: bool = False
):
    if parent_dir is None:
        parent_dir = os.getcwd()

    project_dir = create_folder(parent_dir, project_name, overwrite)

    top_level_dirs = tuple(
        map(
            lambda x: create_folder(project_dir, x, overwrite),
            (FolderType.CORE, FolderType.TEST, FolderType.MOCKS),
        )
    )
    create_folder(project_dir, FolderType.DRIVERS, overwrite)

    for directory in top_level_dirs:
        for folder in (FolderType.INC, FolderType.SRC):
            create_folder(directory, folder, overwrite)

    test_dir = next(
        filter(lambda x: x.split("/")[-1] == "Test", top_level_dirs)
    )
    create_folder(test_dir, FolderType.RUNNERS, overwrite)
    return project_dir


class TooDeepError(Exception):
    def __init__(self, limit):
        self.limit = limit
        super(TooDeepError, self).__init__(self.msg())

    def msg(self):
        return (
            f"Could not find the intended directory "
            f"within {self.limit} levels of the directory "
            f"this function was called from"
        )


def find_sub_dir(
    parent_dir: str, dir_name: str, max_climb: int = 2, _level=0
) -> str:
    if parent_dir.split("/")[-1] != dir_name:
        try:
            ret = next(sub_dir_gen(parent_dir, dir_name))
        except StopIteration:
            if _level <= max_climb:
                ret = find_sub_dir(
                    get_parent_dir(parent_dir), dir_name, max_climb, _level + 1
                )
            else:
                raise TooDeepError(max_climb)
    else:
        ret = parent_dir
    return ret


def sub_dir_gen(parent_dir: str, dir_name: str):
    try:
        sub_dirs = os.listdir(parent_dir)
        if dir_name not in sub_dirs:
            for sub_dir in sub_dirs:
                yield from sub_dir_gen(
                    os.path.join(parent_dir, sub_dir), dir_name
                )
        else:
            yield os.path.join(parent_dir, dir_name)
    except NotADirectoryError:
        pass


def find_all_directories(parent_dir: str, dir_name: str) -> tuple:
    return tuple(sub_dir_gen(parent_dir, dir_name))


def get_parent_dir(dir_name: str):
    split = dir_name.split("/")
    return "/".join(split[:-1])


def add_driver_structure(driver_name: str, drivers_dir: str = None):
    if drivers_dir is None:
        parent_dir = os.getcwd()
        drivers_dir = find_sub_dir(parent_dir, FolderType.DRIVERS)
    new_driver_dir = create_folder(drivers_dir, driver_name)
    for folder in (FolderType.INC, FolderType.SRC):
        create_folder(new_driver_dir, folder)
    return new_driver_dir
