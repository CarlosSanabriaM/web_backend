import configparser
import sys
from os import path, environ

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


def get_param_value_from_conf_file(section: str, param: str) -> str:
    """
    Returns the value of the specified param from the x-conf.ini file.

    * The x-conf.ini file contains configuration for the development environment
    * The production-conf.ini file contains configuration for the production environment

    The absolute path to the x-conf.ini file must be specified in the environment variable CONF_INI_FILE_PATH.

    * In Unix and MacOS, this can be done with the following command: 'export CONF_INI_FILE_PATH=<path/to/x-conf.ini>'
    * In Windows, this can be done with the following command: 'set CONF_INI_FILE_PATH=<path/to/x-conf.ini>'

    The x-conf.ini file contains some configuration strings. \
    Most of them are paths to some files/folders used by the backend, \
    and that need to be modified manually to point to the location of those files/folders \
    in the filesystem where the backend is executed.

    :param section: Name of the section in the x-conf.ini file. For example: '[MALLET]'.
    :param param: Name of the param inside that section. For example: 'SOURCE_CODE_PATH'.
    :return: A str with the value specified in the x-conf.ini file for that param.

    Example:

    ; development-conf.ini

    [MALLET]

    SOURCE_CODE_PATH = /path/to/mallet

    To access that value, execute:

    >>> get_param_value_from_conf_file('MALLET', 'SOURCE_CODE_PATH')

    """
    # Obtain the path to the x-conf.ini file from the CONF_INI_FILE_PATH environment variable
    try:
        conf_ini_file_path = environ['CONF_INI_FILE_PATH']
    except KeyError:
        print(
            "\nThe absolute path to the x-conf.ini file must be specified in the environment variable CONF_INI_FILE_PATH."
            "\nIn development, the development-conf.ini file should be used."
            "\nIn production, the production-conf.ini file should be used."
            "\nTo specify the path in Unix and MacOS, use the command: 'export CONF_INI_FILE_PATH=<path/to/x-conf.ini>'"
            "\nTo specify the path in Windows, use the command: 'set CONF_INI_FILE_PATH=<path/to/x-conf.ini>'"
        )
        # Finish the program
        sys.exit(1)

    config = configparser.ConfigParser()
    config.read(conf_ini_file_path)

    return config[section][param]


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
