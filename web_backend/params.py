import yaml

from web_backend.utils import get_abspath_from_project_source_root

_PARAMS_FILE_PATH = get_abspath_from_project_source_root('params-file.yaml')


def _load_yaml_file(yaml_file_path):
    """
    Loads the specified yaml file into a python dict.

    :param yaml_file_path: Path to the yaml file
    :return: The yaml file as a python dict.
    """
    with open(yaml_file_path, 'r') as yaml_file:
        # Convert the yaml file to a python dict
        return yaml.load(yaml_file, Loader=yaml.SafeLoader)


def get_param(name: str, yaml_file_path: str = None) -> int:
    """
    Returns the value of the param with the specified name from a yaml file.

    Example
    -------
    get_param('topics.text.num_keywords.default') loads the value 5 from the following params file:

    topics:
        text:
            num_keywords:
                default: 5
    text:
        default: 10

    :param name: Name of the parameter, using '.' to separate keys.
    :param yaml_file_path: Path to the params file.
    :return: Value of the parameter obtained from the params-file.yaml file.
    """

    if yaml_file_path is None:
        yaml_file_path = _PARAMS_FILE_PATH

    # Load the yaml file into a python dict
    yaml_file_obj = _load_yaml_file(yaml_file_path)

    # Obtain the keys from the str
    keys = name.split('.')

    # Iterate into the dicts using the keys
    param_value = yaml_file_obj
    for key in keys:
        param_value = param_value[key]

    # Return the value of the last dict
    return param_value


def update_param(name: str, value: int, yaml_file_path: str = None):
    if yaml_file_path is None:
        yaml_file_path = _PARAMS_FILE_PATH

    # Load the yaml file into a python dict
    yaml_file_obj = _load_yaml_file(yaml_file_path)

    # Obtain the keys from the str
    keys = name.split('.')

    # Iterate into the dicts using the keys, except the last key
    param_dict = yaml_file_obj
    for key in keys[:len(keys) - 1]:
        param_dict = param_dict[key]

    # Update the inner dict with the value
    param_dict[keys[-1]] = value

    # Rewrite the yaml file with the new dict
    with open(yaml_file_path, 'w') as yaml_file:
        yaml.dump(yaml_file_obj, yaml_file)
