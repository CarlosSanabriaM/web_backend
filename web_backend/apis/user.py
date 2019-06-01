from typing import Any, Dict, List

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import abort

from web_backend.utils import UserInvalidParamError, UserResourceWithParamValueNotFoundError
from web_backend.wrapper.twenty_news_groups_dataset_models_wrapper import TwentyNewsGroupsDatasetModelsWrapper

user_api = Blueprint('user_api', __name__, url_prefix='/user/api', static_url_path='/static')

models_wrapper = TwentyNewsGroupsDatasetModelsWrapper()


@user_api.route('/')
def user_api_running_message():
    """
    If the User API is running, returns a JSON response.
    """
    return jsonify(user_api_running=True)  # 200 OK


@user_api.route('/topics/text')
def get_topics_text():
    """
    REST API endpoint that returns the most important keywords of each topic, and their probabilities.

    The endpoint can only be called with a HTTP GET method.

    Admits a param in the URL called num_keywords: int (endpoint?num_keywords=10, for example).

    If the num_keywords param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the num_keywords param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_keywords = request.args.get('num_keywords', type=int)

    try:
        # Try to obtain the topics in text format.
        return jsonify(models_wrapper.get_topics_text(num_keywords))  # 200 OK
    except UserInvalidParamError as err:
        # If num_keywords doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


@user_api.route('/topics/wordcloud')
def get_topics_word_cloud_images_urls():
    """
    REST API endpoint that, for each topic, returns a url that points to a wordcloud image of that topic.

    The endpoint can only be called with a HTTP GET method.

    Admits a param in the URL called num_keywords: int (endpoint?num_keywords=10, for example).

    If the num_keywords param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the num_keywords param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_keywords = request.args.get('num_keywords', type=int)

    try:
        # Call the ModelsWrapper get_topics_word_cloud_images_urls(), passing it the num_keywords
        topic_image_url_dto_list = models_wrapper.get_topics_word_cloud_images_urls(num_keywords)
        # Transform the List[ReprDocOfTopicDTO] to a list of dicts
        dicts_list = _transform_dto_list_to_list_of_dicts(topic_image_url_dto_list)
        return jsonify(dicts_list)  # 200 OK
    except UserInvalidParamError as err:
        # If num_keywords doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


@user_api.route('/topics/<int:topic_id>/documents')
def get_k_most_repr_docs_of_topic(topic_id: int):
    """
    REST API endpoint that returns info about the most representative documents of the given topic.

    The endpoint can only be called with a HTTP GET method. The URL embedded param topic_id is obligatory.

    The other param that admits is num_documents: int param in the URL (endpoint?num_documents=10, for example).

    If the topic_id param is not present in the topics_model, an error (in JSON format)
    with HTTP 404 status code is returned.

    If the num_documents param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the num_documents param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_documents = request.args.get('num_documents', type=int)

    try:
        # Call the ModelsWrapper get_k_most_repr_docs_of_topic(), passing it the topic_id and the num_documents
        repr_doc_of_topic_dto_list = models_wrapper.get_k_most_repr_docs_of_topic(topic_id, num_documents)
        # Transform the List[ReprDocOfTopicDTO] to a list of dicts
        dicts_list = _transform_dto_list_to_list_of_dicts(repr_doc_of_topic_dto_list)
        return jsonify(dicts_list)  # 200 OK
    except UserInvalidParamError as err:
        # If num_documents doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)
    except UserResourceWithParamValueNotFoundError as err:
        # If a topic with the topic_id specified by the user doesn't exist, send a 404 error message to the user
        abort(404, description=err.message)


@user_api.route('/text/related/topics', methods=['POST'])
def get_text_related_topics():
    """
    REST API endpoint that returns info about the probability of the topics being related with the given text.

    The endpoint can only be called with a HTTP POST method. The params that admits are:

    * A text: str param in the request body
    * A max_num_topics: int param in the URL (endpoint?max_num_topics=10, for example)

    If the max_num_topics param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the text param from the request body
    # If the param is not present Flask sends an automatic response with 400 Bad Request status code
    text: str = request.form['text']

    # Get the max_num_topics param from the request URL
    # If the param is not present or it's type is not int, None is returned
    max_num_topics = request.args.get('max_num_topics', type=int)

    try:
        # Call the ModelsWrapper get_text_related_topics(), passing it the text and the max_num_topics
        text_topic_prob_dto_list = models_wrapper.get_text_related_topics(text, max_num_topics)
        # Transform the List[TextTopicProbDTO] to a list of dicts
        dicts_list = _transform_dto_list_to_list_of_dicts(text_topic_prob_dto_list)
        return jsonify(dicts_list)  # 200 OK
    except UserInvalidParamError as err:
        # If max_num_topics doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


@user_api.route('/text/related/documents', methods=['POST'])
def get_text_related_docs():
    """
    REST API endpoint that returns the documents of the dataset more related to the given text.

    The endpoint can only be called with a HTTP POST method. The params that admits are:

    * A text: str param in the request body
    * A num_documents: int param in the URL (endpoint?num_documents=10, for example)

    If the num_documents param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the text param from the request body
    # If the param is not present Flask sends an automatic response with 400 Bad Request status code
    text: str = request.form['text']

    # Get the num_documents param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_documents = request.args.get('num_documents', type=int)

    try:
        # Call the ModelsWrapper get_text_related_docs(), passing it the text and the num_documents
        text_related_doc_dto_list = models_wrapper.get_text_related_docs(text, num_documents)
        # Transform the List[TextRelatedDocDTO] to a list of dicts
        dicts_list = _transform_dto_list_to_list_of_dicts(text_related_doc_dto_list)
        return jsonify(dicts_list)  # 200 OK
    except UserInvalidParamError as err:
        # If num_documents doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


@user_api.route('/text/summary', methods=['POST'])
def get_text_summary():
    """
    REST API endpoint that summarizes a given text.

    The endpoint can only be called with a HTTP POST method. The params that admits are:

    * A text: str param in the request body
    * A num_summary_sentences: int param in the URL (endpoint?num_summary_sentences=10, for example)

    If the num_summary_sentences param is not valid, an error (in JSON format) with HTTP 422 status code is returned.
    """

    # Get the text param from the request body
    # If the param is not present Flask sends an automatic response with 400 Bad Request status code
    text: str = request.form['text']

    # Get the num_summary_sentences param from the request URL
    # If the param is not present or it's type is not int, None is returned
    num_summary_sentences = request.args.get('num_summary_sentences', type=int)

    try:
        # Call the ModelsWrapper get_text_summary(), passing it the text and the num_summary_sentences
        return jsonify(vars(models_wrapper.get_text_summary(text, num_summary_sentences)))  # 200 OK
    except UserInvalidParamError as err:
        # If num_summary_sentences doesn't have a valid value, send a 422 error message to the user
        abort(422, description=err.message)


def _transform_dto_list_to_list_of_dicts(dto_list) -> List[Dict[str, Any]]:
    """
    Given a list of DTO objects, this function returns a list of dicts, that can be passed to jsonify function.
    """
    return [vars(dto_obj) for dto_obj in dto_list]
