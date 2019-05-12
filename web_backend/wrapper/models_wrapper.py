from topics_and_summary.models.summarization import TextRank
from topics_and_summary.models.topics import TopicsModel, LdaMalletModel
from topics_and_summary.utils import pretty_print

from web_backend.utils import get_abspath_from_project_source_root


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

    def __init__(self, topics_model_name: str, dataset_path: str, model_class=LdaMalletModel,
                 summarization_model_word_embeddings='glove'):
        """
        Loads the TopicsModel and creates the SummarizationModel.

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
