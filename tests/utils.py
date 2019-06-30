from os import path

from web_backend.utils import join_paths

# This python module (utils.py) must be in the root folder of tests package.
TESTS_ROOT_PATH = path.dirname(path.abspath(__file__))


def get_abspath_from_tests_root(_path: str) -> str:
    """
    Returns the absolute path of the relative path passed as a parameter.

    :param _path: Path relative from the tests root directory.
    """
    return path.abspath(join_paths(TESTS_ROOT_PATH, _path))
