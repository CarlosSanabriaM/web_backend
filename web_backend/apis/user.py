from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from web_backend.utils import UserError
from web_backend.wrapper.twenty_news_groups_dataset_models_wrapper import TwentyNewsGroupsDatasetModelsWrapper

user_api = Blueprint('user_api', __name__, url_prefix='/user/api', static_url_path='/static')

models_wrapper = TwentyNewsGroupsDatasetModelsWrapper()


@user_api.route('/')
def user_api_message():
    return jsonify(user_api_running='yes')  # 200 OK


@user_api.route('/topics/text')
def get_topics_text():
    # Get the num_keywords param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_keywords = request.args.get('num_keywords', type=int)

    try:
        # Try to obtain the topics in text format.
        topics_list = models_wrapper.get_topics_text(num_keywords)
        # Convert the List[Topic] in the following JSON:
        # [{"topic": 0, "keywords": [{"keyword": "god", "probability": 0.87}, ...]}, ...]
        raise NotImplementedError

    except UserError as err:
        # If num_keywords doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


@user_api.route('/topics/wordcloud')
def get_topics_word_cloud_images_urls():
    raise NotImplementedError


@user_api.route('/topics/<int:topic_id>/documents')
def get_k_most_repr_docs_of_topic(topic_id: int):
    raise NotImplementedError


@user_api.route('/text/related/topics', methods=['POST'])
def get_text_related_topics():
    raise NotImplementedError


@user_api.route('/text/related/documents', methods=['POST'])
def get_text_related_docs():
    raise NotImplementedError


@user_api.route('/text/summary', methods=['POST'])
def get_text_summary():
    """
    REST API endpoint that only can be called with a HTTP POST method. The params that admits are:

    * A text: str param in the request body
    * A num_summary_sentences: int param in the URL

    If the num_summary_sentences param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the text param from the request body
    # If the param is not present Flask sends an automatic response with 400 Bad Request status code
    text: str = request.form['text']

    # Get the num_summary_sentences param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_summary_sentences = request.args.get('num_summary_sentences', type=int)

    # Call the ModelsWrapper get_text_summary(), passing it the text and the num_summary_sentences
    try:
        return jsonify(vars(models_wrapper.get_text_summary(text, num_summary_sentences)))  # 200 OK
    except UserError as err:
        # If num_summary_sentences doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)
