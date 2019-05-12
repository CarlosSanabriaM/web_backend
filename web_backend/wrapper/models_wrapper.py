import os
from typing import List

from topics_and_summary.models.summarization import TextRank
from topics_and_summary.models.topics import TopicsModel, LdaMalletModel, Topic
from topics_and_summary.utils import pretty_print
from topics_and_summary.visualizations import plot_word_clouds_of_topics

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
            num_keywords = get_param(param_name + '.default')
        else:
            param_min_value = get_param(param_name + '.min')
            param_max_value = get_param(param_name + '.max')

            if num_keywords < param_min_value or num_keywords > param_max_value:
                raise UserError('num_keywords param must be in the range [{0},{1}]'
                                .format(param_min_value, param_max_value))

        return self.topics_model.get_topics(num_keywords)

    def get_topics_word_cloud_images_urls(self, num_keywords: int = None):
        # Obtain the params values from the params file
        param_name = 'topics.wordcloud.num_keywords'

        if num_keywords is None:
            num_keywords = get_param(param_name + '.default')
        else:
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
                                       dpi=200)

        # Return a dictionary {'topicx': 'path/to/topicx-image.png'}, with paths relative to the static folder
        num_keywords_dir_relative_path = wordcloud_images_num_keywords_dir.split('static/')[1]
        topic_wordcloud_image_relative_path = join_paths(num_keywords_dir_relative_path, 'topic{}.png')
        paths_dict = {
            'topic{}'.format(topic): topic_wordcloud_image_relative_path.format(topic)
            for topic in range(self.topics_model.num_topics)
        }

        return paths_dict

    def get_k_most_repr_docs_of_topic(self):
        raise NotImplementedError

    def get_text_related_topics(self):
        raise NotImplementedError

    def get_text_related_docs(self):
        raise NotImplementedError

    def get_text_summary(self):
        raise NotImplementedError
