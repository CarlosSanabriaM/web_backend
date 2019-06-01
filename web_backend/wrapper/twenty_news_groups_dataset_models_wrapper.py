from topics_and_summary.models.topics import LdaMalletModel

from web_backend.utils import get_param_value_from_conf_file
from web_backend.wrapper.models_wrapper import ModelsWrapper


class TwentyNewsGroupsDatasetModelsWrapper(ModelsWrapper):
    """
    Class that wraps the functionality of the topics_and_summary library, specifically for the 20 NewsGroups dataset.

    This class specifies the class of the best model for the 20 NewsGroups dataset,
    and also loads the name of the best model and the path to the 20 NewsGroups dataset original documents
    from the configuration file.

    Topics models must have been previously generated using the topics_and_summary library and
    must be previously stored in the TOPICS_MODELS_DIR_PATH folder.
    """

    BEST_TOPICS_MODEL_CLASS = LdaMalletModel
    """ Class of the best topics model. """

    def __init__(self, topics_model_name=None, dataset_path: str = None,
                 model_class=BEST_TOPICS_MODEL_CLASS, summarization_model_word_embeddings='glove'):
        """
        Specifies default values that are passed to ModelsWrapper() to easily use the 20Newsgroups dataset.

        :param topics_model_name: Name of the topics_model stored in the TOPICS_MODELS_DIR_PATH folder. \
        If is None, the value is loaded from the *-conf.ini file.
        :param dataset_path: Path to the folder that contains the original dataset documents. \
        If is None, the value is loaded from the *-conf.ini file.
        :param model_class: TopicsModel class of the model with name topics_model_name \
        stored in the TOPICS_MODELS_DIR_PATH folder. It must be a subclass of TopicsModel. For example:

        >>> from topics_and_summary.models.topics import LdaMalletModel
        >>> wrapper = TwentyNewsGroupsDatasetModelsWrapper('name', model_class=LdaMalletModel)

        :param summarization_model_word_embeddings: Word embeddings to be used by the summarization model. \
        Possible values are: 'glove' or 'word2vec'.
        """

        if topics_model_name is None:
            # Load topics_model_name from the *-conf.ini file
            topics_model_name = get_param_value_from_conf_file('MODELS', 'BEST_TOPICS_MODEL_NAME')
        if dataset_path is None:
            # Load twenty_newsgroups_dataset_path from the *-conf.ini file
            dataset_path = get_param_value_from_conf_file('DATASETS', 'TWENTY_NEWS_GROUPS_DIR_PATH')

        super().__init__(topics_model_name, dataset_path, model_class, summarization_model_word_embeddings)
