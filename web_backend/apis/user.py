from flask import Blueprint

user_api = Blueprint('user_api', __name__, url_prefix='/user/api')


@user_api.route('/')
def user_api_message():
    return 'User API'
