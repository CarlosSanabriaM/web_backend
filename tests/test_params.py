import unittest
from os import remove
from shutil import copyfile

from tests.utils import get_abspath_from_tests_root
from web_backend.params import get_param, update_param


class TestParams(unittest.TestCase):
    _PARAMS_TEST_FILE_PATH = get_abspath_from_tests_root('params-test-file.yaml')
    _PARAMS_TEST_UPDATE_FILE_PATH = get_abspath_from_tests_root('params-test-update-file.yaml')

    def test_get_param(self):
        """
        Loads param values from the yaml test file and checks if the values are the expected.
        """
        self.assertEqual(get_param('topics.text.num_keywords.default', self._PARAMS_TEST_FILE_PATH), 5)
        self.assertEqual(get_param('topics.text.num_keywords.min', self._PARAMS_TEST_FILE_PATH), 1)
        self.assertEqual(get_param('topics.text.num_keywords.max', self._PARAMS_TEST_FILE_PATH), 30)

        self.assertEqual(get_param('text.num_related_documents.default', self._PARAMS_TEST_FILE_PATH), 6)
        self.assertEqual(get_param('text.num_related_documents.min', self._PARAMS_TEST_FILE_PATH), 1)
        self.assertEqual(get_param('text.num_related_documents.max', self._PARAMS_TEST_FILE_PATH), 20)

    def test_update_param(self):
        """
        Updates some param values of a copy of the yaml test file and checks if they have been correctly modified, \
        without modifying others.
        """
        # Create a copy of the params-file.yaml
        copyfile(self._PARAMS_TEST_FILE_PATH, self._PARAMS_TEST_UPDATE_FILE_PATH)

        # Update some params of the file copied
        update_param('topics.text.num_keywords.default', 1000, self._PARAMS_TEST_UPDATE_FILE_PATH)
        update_param('topics.text.num_keywords.min', 999, self._PARAMS_TEST_UPDATE_FILE_PATH)
        update_param('topics.text.num_keywords.max', 998, self._PARAMS_TEST_UPDATE_FILE_PATH)

        update_param('text.num_related_documents.default', 997, self._PARAMS_TEST_UPDATE_FILE_PATH)
        update_param('text.num_related_documents.min', 996, self._PARAMS_TEST_UPDATE_FILE_PATH)
        update_param('text.num_related_documents.max', 995, self._PARAMS_TEST_UPDATE_FILE_PATH)

        # Check that the values of those params have been updated
        self.assertEqual(get_param('topics.text.num_keywords.default', self._PARAMS_TEST_UPDATE_FILE_PATH), 1000)
        self.assertEqual(get_param('topics.text.num_keywords.min', self._PARAMS_TEST_UPDATE_FILE_PATH), 999)
        self.assertEqual(get_param('topics.text.num_keywords.max', self._PARAMS_TEST_UPDATE_FILE_PATH), 998)

        self.assertEqual(get_param('text.num_related_documents.default', self._PARAMS_TEST_UPDATE_FILE_PATH), 997)
        self.assertEqual(get_param('text.num_related_documents.min', self._PARAMS_TEST_UPDATE_FILE_PATH), 996)
        self.assertEqual(get_param('text.num_related_documents.max', self._PARAMS_TEST_UPDATE_FILE_PATH), 995)

        # Check that other values haven't been modified
        self.assertEqual(get_param('topics.wordcloud.num_keywords.default', self._PARAMS_TEST_UPDATE_FILE_PATH), 10)
        self.assertEqual(get_param('topics.wordcloud.num_keywords.min', self._PARAMS_TEST_UPDATE_FILE_PATH), 1)
        self.assertEqual(get_param('topics.wordcloud.num_keywords.max', self._PARAMS_TEST_UPDATE_FILE_PATH), 100)

        # Remove the yaml copy file
        remove(self._PARAMS_TEST_UPDATE_FILE_PATH)


if __name__ == '__main__':
    unittest.main()
