import os
from typing import List, Dict, Tuple

from networkx import PowerIterationFailedConvergence
from nltk import sent_tokenize
from topics_and_summary.models.summarization import TextRank
from topics_and_summary.models.topics import TopicsModel, LdaMalletModel, Topic
from topics_and_summary.utils import pretty_print
from topics_and_summary.visualizations import plot_word_clouds_of_topics
from tqdm import tqdm

from web_backend.params import get_param
from web_backend.utils import get_abspath_from_project_source_root, UserError, join_paths


class ModelsWrapper:
    """
    Class that wraps the functionality of the topics_and_summary library.

    Topics models must have been previously generated using the topics_and_summary library and stored in the
    TOPICS_MODELS_DIR_PATH folder.
    """

    TOPICS_MODELS_DIR_PATH = get_abspath_from_project_source_root('saved-elements/models/topics')
    # TODO: Change this paths in production!
    MALLET_SOURCE_CODE_PATH = get_abspath_from_project_source_root('../../topics_and_summary/mallet-2.0.8/bin/mallet')
    WORD2VEC_EMBEDDINGS_PATH = get_abspath_from_project_source_root(
        '../../topics_and_summary/embeddings/word2vec/GoogleNews-vectors-negative300.bin.gz')
    GLOVE_EMBEDDINGS_DIR_PATH = get_abspath_from_project_source_root(
        '../../topics_and_summary/embeddings/glove/glove.6B')
    WORDCLOUD_IMAGES_DIR_PATH = get_abspath_from_project_source_root('static/wordcloud-images')

    def __init__(self, topics_model_name: str, dataset_path: str, model_class=LdaMalletModel,
                 summarization_model_word_embeddings='glove'):
        """
        Loads the TopicsModel and creates the SummarizationModel. It also generates the wordcloud images and stores
        them in the static/wordcloud-images folder.

        :param topics_model_name: Name of the topics_model stored in the TOPICS_MODELS_DIR_PATH folder.
        :param dataset_path: Path to the folder that contains the original dataset documents.
        :param model_class: TopicsModel class of the model with name topics_model_name \
        stored in the TOPICS_MODELS_DIR_PATH folder. It must be a subclass of TopicsModel. For example:

        >>> from topics_and_summary.models.topics import LdaMalletModel
        >>> wrapper = ModelsWrapper('name', model_class=LdaMalletModel)

        :param summarization_model_word_embeddings: Word embeddings to be used by the summarization model. \
        Possible values are: 'glove' or 'word2vec'.
        """

        # Load topics model from disk
        if not issubclass(model_class, TopicsModel) or not model_class != TopicsModel:
            raise Exception('Wrong value for parameter model_class.\n'
                            'Given value: {0}\n'
                            'It must be a subclass of the topics_and_summary.models.topics.TopicsModel class.'
                            .format(model_class))
        elif model_class == LdaMalletModel:
            pretty_print('Loading the Topics Model')
            # LdaMalletModel has a different load method (has a mallet_path param)
            model_class: LdaMalletModel
            self.topics_model = model_class.load(topics_model_name,
                                                 model_parent_dir_path=self.TOPICS_MODELS_DIR_PATH,
                                                 dataset_path=dataset_path,
                                                 mallet_path=self.MALLET_SOURCE_CODE_PATH)
        else:
            pretty_print('Loading the Topics Model')
            model_class: TopicsModel
            self.topics_model = model_class.load(topics_model_name,
                                                 model_parent_dir_path=self.TOPICS_MODELS_DIR_PATH,
                                                 dataset_path=dataset_path)

        # Create the summarization model
        pretty_print('Creating the TextRank model')
        if summarization_model_word_embeddings == 'glove':
            self.summarization_model = TextRank(embedding_model='glove',
                                                embeddings_path=self.GLOVE_EMBEDDINGS_DIR_PATH)
        elif summarization_model_word_embeddings == 'word2vec':
            self.summarization_model = TextRank(embedding_model='word2vec',
                                                embeddings_path=self.WORD2VEC_EMBEDDINGS_PATH)
        else:
            raise Exception('Wrong value for parameter summarization_model_word_embeddings.\n'
                            'Given value: {0}\n'
                            'Possible values: "glove" or "word2vec"'.format(summarization_model_word_embeddings))

    def get_topics_text(self, num_keywords: int = None) -> List[Topic]:
        """
        Returns the topics of the TopicsModel in text format.

        If num_keywords has no value, the default value is obtained from the params file.

        If num_keywords value is lesser than the min value for this param or is greater than the max value
        for this param (both specified in the params file) a UserError exception is raised.

        :return: A list of Topic's objects with the topics of the TopicsModel.
        """

        # Obtain the params values from the params file
        param_name = 'topics.text.num_keywords'

        if num_keywords is None:
            # If num_keywords has no value, give it the default one
            num_keywords = get_param(param_name + '.default')
        else:
            # If num_keywords has value, check if it's inside the valid range
            param_min_value = get_param(param_name + '.min')
            param_max_value = get_param(param_name + '.max')

            if num_keywords < param_min_value or num_keywords > param_max_value:
                raise UserError('num_keywords param must be in the range [{0},{1}]'
                                .format(param_min_value, param_max_value))

        return self.topics_model.get_topics(num_keywords)

    def get_topics_word_cloud_images_urls(self, num_keywords: int = None) -> Dict[str, str]:
        """
        Returns a dict with the following structure:

        * key (str): 'topic<topic-id>'
        * value (str): 'path/to/topic<topic-id>-image.png', with paths relative to the static folder

        If wordcloud images with the same num_keywords have been previously generated, they are not generated again.
        If not, they are generated and stored inside a new folder <num_keywords>keywords. This new folder is created
        inside the WORDCLOUD_IMAGES_DIR_PATH folder.

        If num_keywords has no value, the default value is obtained from the params file.

        If num_keywords value is lesser than the min value for this param or is greater than the max value
        for this param (both specified in the params file) a UserError exception is raised.

        :return: A dict with relative paths to the images as explained above.
        """

        # Obtain the params values from the params file
        param_name = 'topics.wordcloud.num_keywords'

        if num_keywords is None:
            # If num_keywords has no value, give it the default one
            num_keywords = get_param(param_name + '.default')
        else:
            # If num_keywords has value, check if it's inside the valid range
            param_min_value = get_param(param_name + '.min')
            param_max_value = get_param(param_name + '.max')

            if num_keywords < param_min_value or num_keywords > param_max_value:
                raise UserError('num_keywords param must be in the range [{0},{1}]'
                                .format(param_min_value, param_max_value))

        wordcloud_images_num_keywords_dir = join_paths(self.WORDCLOUD_IMAGES_DIR_PATH,
                                                       '{}keywords'.format(num_keywords))

        # If there is a folder with the same num_keywords inside the wordcloud-images,
        # that means that images with that num_keywords have been previously generated.
        # The images are generated only if the folder doesn't exist.
        if not os.path.exists(wordcloud_images_num_keywords_dir):
            pretty_print('Generating and storing the wordcloud images in ' + wordcloud_images_num_keywords_dir)
            os.mkdir(wordcloud_images_num_keywords_dir)
            plot_word_clouds_of_topics(self.topics_model.get_topics(num_keywords), single_plot_per_topic=True,
                                       show_plot=False, save=True, dir_save_path=wordcloud_images_num_keywords_dir,
                                       save_base_name='topic', dpi=200)

        # Return a dictionary {'topicx': 'path/to/topicx-image.png'}, with paths relative to the static folder
        num_keywords_dir_relative_path = wordcloud_images_num_keywords_dir.split('static/')[1]
        topic_wordcloud_image_relative_path = join_paths(num_keywords_dir_relative_path, 'topic{}.png')
        paths_dict = {
            'topic{}'.format(topic): topic_wordcloud_image_relative_path.format(topic)
            for topic in range(self.topics_model.num_topics)
        }

        return paths_dict

    def _summarize_text(self, text: str, num_summary_sentences: int) -> Tuple[str, bool]:
        """
        Given a text and a number of sentences, this function tries to generate a summary of the text with \
        that number of sentences using the SummarizationModel.

        If the SummarizationModel doesn't converge, this function selects the first num_summary_sentences sentences \
        as a summary.

        :param text: Text to be summarized.
        :param num_summary_sentences: Number of sentences of the summary.
        :return: A tuple (summary, summary_generated_with_the_model). If summary_generated_with_the_model is True,
        that means that the summary was generated with the Summarization model. Else, that means that the summary
        contains the first num_summary_sentences sentences of the given text.
        """

        # Try to generate the summary using the summarization_model
        try:
            text_summary = self.summarization_model.get_k_best_sentences_of_text(text, num_summary_sentences)
            summary_generated_with_the_model = True
        except PowerIterationFailedConvergence:
            # If the SummarizationModel doesn't converge, select the first num_summary_sentences sentences as a summary
            text_sentences = sent_tokenize(text)
            text_summary = text_sentences[:num_summary_sentences]
            summary_generated_with_the_model = False

        # Transform the summary from a List[str] to a str
        text_summary = '\n'.join(text_summary)

        return text_summary, summary_generated_with_the_model

    def get_k_most_repr_docs_of_topic(self, topic: int, num_docs: int = None) -> List['ReprDocOfTopic']:
        """
        Given a topic-id and a number of documents, this function returns a List[ReprDocOfTopic] with info
        about the num_docs most representative documents of the given topic. Of each document, ReprDocOfTopic stores:

        * The document original content
        * A summary of the document original content
        * The document-topic probability

        :param topic: Topic id in the range [0,num_topics-1]
        :param num_docs:
        :return:
        """

        # Check if the topic id has a valid value
        if topic < 0 or topic > self.topics_model.num_topics - 1:
            raise UserError('topic param must be in the range [{0},{1}]'
                            .format(0, self.topics_model.num_topics - 1))

        # Obtain the params values from the params file
        param_name = 'topics.documents.num_documents'

        if num_docs is None:
            # If num_docs has no value, give it the default one
            num_docs = get_param(param_name + '.default')
        else:
            # If num_docs has value, check if it's inside the valid range
            param_min_value = get_param(param_name + '.min')
            param_max_value = get_param(param_name + '.max')

            if num_docs < param_min_value or num_docs > param_max_value:
                raise UserError('num_docs param must be in the range [{0},{1}]'
                                .format(param_min_value, param_max_value))

        # Obtain the num_docs most representative document of the given topic as a pandas DataFrame
        k_most_repr_docs_of_topic_df = self.topics_model.get_k_most_repr_docs_of_topic_as_df(topic, k=num_docs)

        # Obtain the num_summary_sentences param specific for the most representative documents
        num_summary_sentences = get_param('topics.documents.num_summary_sentences.default')

        # Get the info from the DataFrame, generate the summaries and store each doc info inside a ReprDocOfTopic object
        repr_doc_of_topic_list = []
        progress_bar = tqdm(range(num_docs))
        for i in progress_bar:
            progress_bar.set_description('Selecting document content and generating summaries')
            # Obtain the document content
            doc_content = k_most_repr_docs_of_topic_df['Original doc text'][i]
            # Generate the document content summary
            doc_content_summary, _ = self._summarize_text(doc_content, num_summary_sentences)
            # In this function, the second value returned by _summarize_text() is not used,
            # because here the summary of a document is something secondary/accessory, and it doesn't really
            # matter if the summary was generated with the SummarizationModel or not.

            # Obtain the document-topic probability
            doc_topic_prob = k_most_repr_docs_of_topic_df['Topic prob'][i]

            repr_doc_of_topic_list.append(ReprDocOfTopic(doc_content, doc_content_summary, doc_topic_prob))

        return repr_doc_of_topic_list

    def get_text_related_topics(self):
        raise NotImplementedError

    def get_text_related_docs(self):
        raise NotImplementedError

    def get_text_summary(self):
        raise NotImplementedError


class ReprDocOfTopic:
    """
    DTO that stores the information about one of the most representative documents of a topic.

    Instances of this class are created inside the get_k_most_repr_docs_of_topic() method.

    The apis/user module will use this class to access the info returned by get_k_most_repr_docs_of_topic().
    """

    def __init__(self, doc_content: str, doc_content_summary: str, doc_topic_prob: float):
        self.doc_content = doc_content
        self.doc_content_summary = doc_content_summary
        self.doc_topic_prob = doc_topic_prob
