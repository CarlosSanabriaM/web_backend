import unittest

from nltk import sent_tokenize

from web_backend.wrapper.twenty_news_groups_dataset_models_wrapper import TwentyNewsGroupsDatasetModelsWrapper


class TestModelsWrapper(unittest.TestCase):
    _TEXT_DOESNT_CONVERGE_FILE_PATH = 'text-doesnt-converge.txt'
    _TEXT_CONVERGES_FILE_PATH = 'text-converges.txt'

    @classmethod
    def setUpClass(cls) -> None:
        cls.wrapper = TwentyNewsGroupsDatasetModelsWrapper()

    def test_summarize_text_doesnt_converge(self):
        """
        Check that the _summarize_text() method returns the first num_summary_sentences sentences of a
        text that doesn't converge with the TextRank SummarizationModel.
        """
        # Load the text from a file
        with open(self._TEXT_DOESNT_CONVERGE_FILE_PATH) as f:
            text = f.read()

        # Try to generate a summary of the text with 4 sentences
        num_summary_sentences = 4
        summary, summary_generated_with_the_model = self.wrapper._summarize_text(text, num_summary_sentences)

        # Check that the summary wasn't generated with the model
        self.assertEqual(False, summary_generated_with_the_model)

        # Check that the summary contains num_summary_sentences sentences
        summary_sentences = sent_tokenize(summary)
        self.assertEqual(num_summary_sentences, len(summary_sentences))

        # Check that the summary contains the num_summary_sentences first sentences of the text
        text_sentences = sent_tokenize(text)
        for i, summary_sent in enumerate(summary_sentences):
            self.assertEqual(text_sentences[i], summary_sent)

    def test_summarize_text_converges(self):
        """
        Check that the _summarize_text() method doesn't return the first num_summary_sentences sentences of a
        text that converges with the TextRank SummarizationModel.

        **Note:** The algorithm could return the first num_summary_sentences sentences if they are very important
        in the text, but in this test we have chosen a text in which that doesn't happen.
        """
        # Load the text from a file
        with open(self._TEXT_CONVERGES_FILE_PATH) as f:
            text = f.read()

        # Try to generate a summary of the text with 4 sentences
        num_summary_sentences = 4
        summary, summary_generated_with_the_model = self.wrapper._summarize_text(text, num_summary_sentences)

        # Check that the summary was generated with the model
        self.assertEqual(True, summary_generated_with_the_model)

        # Check that the summary contains num_summary_sentences sentences
        summary_sentences = sent_tokenize(summary)
        self.assertEqual(num_summary_sentences, len(summary_sentences))

        # Check that the summary doesn't contain the num_summary_sentences first sentences of the text
        text_sentences = sent_tokenize(text)
        at_least_one_sentence_is_different = False
        for i, summary_sent in enumerate(summary_sentences):
            at_least_one_sentence_is_different = at_least_one_sentence_is_different or text_sentences[i] != summary_sent
        self.assertEqual(True, at_least_one_sentence_is_different)


if __name__ == '__main__':
    unittest.main()
