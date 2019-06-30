"""
Module to run all tests.

This module should only be used by the Coverage.py module to generate tests coverage and tests reports,
because the results this module gives to the user about the tests execution are worst than the ones given by the PyCharm IDE.

In PyCharm, to execute all tests and see the results properly, right click the tests folder
and select "Run 'unittests in tests'" option.
"""

import os
import unittest

from web_backend.utils import join_paths

if __name__ == '__main__':
    loader = unittest.TestLoader()

    tests_dir_path = os.path.abspath(join_paths(__file__, os.pardir))

    # If the environment variable CONF_INI_FILE_PATH is not set, set it here with the development file
    if not 'CONF_INI_FILE_PATH' in os.environ:
        conf_ini_file_path = os.path.abspath(join_paths(tests_dir_path, os.pardir, 'development-conf.ini'))
        os.environ['CONF_INI_FILE_PATH'] = conf_ini_file_path

    # Obtain a suit of tests with all the tests in the tests directory
    suite = loader.discover(tests_dir_path)

    # Run all tests
    runner = unittest.TextTestRunner()
    runner.run(suite)
