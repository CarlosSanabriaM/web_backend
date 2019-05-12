from topics_and_summary.models.topics import LdaMalletModel

from web_backend.utils import get_abspath_from_project_source_root
from web_backend.wrapper.models_wrapper import ModelsWrapper


class TwentyNewsGroupsDatasetModelsWrapper(ModelsWrapper):
    """
    Class that wraps the functionality of the topics_and_summary library, specifically for the 20 NewsGroups dataset.

    This class specifies the name and class of the best model for the 20 NewsGroups dataset, and also the path
    to the 20 NewsGroups dataset original documents.

    Topics models must have been previously generated using the topics_and_summary library and stored in the
    TOPICS_MODELS_DIR_PATH folder.
    """

    BEST_TOPICS_MODEL_NAME = 'lda_mallet_17topics_model'
    BEST_TOPICS_MODEL_CLASS = LdaMalletModel
    # TODO: Change this path in production!
    TWENTY_NEWS_GROUPS_DATASET_DIR_PATH = get_abspath_from_project_source_root(
        '../../topics_and_summary/datasets/20_newsgroups')

    def __init__(self, topics_model_name=BEST_TOPICS_MODEL_NAME, dataset_path: str = None,
                 model_class=BEST_TOPICS_MODEL_CLASS, summarization_model_word_embeddings='glove'):
        if dataset_path is None:
            dataset_path = self.TWENTY_NEWS_GROUPS_DATASET_DIR_PATH

        super().__init__(topics_model_name, dataset_path, model_class, summarization_model_word_embeddings)
