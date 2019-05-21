from os import path

# This python module (utils.py) must be in the root folder of the python package project.
PROJECT_SOURCE_ROOT_PATH = path.dirname(path.abspath(__file__))


def join_paths(path1: str, *paths: str) -> str:
    """
    Joins 2 paths. If paths contains '/', transform to '\\' if os is Windows.
    """
    # If paths contains '/', transform to '\\' if os is Windows.
    path1 = path.normcase(path1)
    paths = map(lambda p: path.normcase(p), paths)

    # Join all the paths
    return path.join(path1, *paths)


def get_abspath_from_project_source_root(_path: str) -> str:
    """
    Returns the absolute path of the relative path passed as a parameter.

    :param _path: Path relative from the project source root (folder that contains an __init__.py file \
    and the rest of the Python packages and modules).
    """
    return path.abspath(join_paths(PROJECT_SOURCE_ROOT_PATH, _path))


def rename_attribute(obj, old_attribute_name, new_attribute_name):
    """
    Given a object, this function renames one of it's attributes.
    """
    setattr(obj, new_attribute_name, getattr(obj, old_attribute_name))
    delattr(obj, old_attribute_name)


class UserError(Exception):
    """
    Exception for raising user errors.

    The exception contains a message attribute.
    """

    def __init__(self, message):
        """
        :param message: Message of the Error.
        """
        self.message = message


class UserInvalidParamError(UserError):
    """
    Exception for raising user errors, when param value introduced by the user is invalid.

    The exception contains a message attribute.
    """


class UserResourceWithParamValueNotFoundError(UserError):
    """
    Exception for raising user errors, when param value introduced by the user doesn't found any resource.

    The exception contains a message attribute.
    """
