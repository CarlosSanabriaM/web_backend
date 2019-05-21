from flask import Blueprint, jsonify

admin_api = Blueprint('admin_api', __name__, url_prefix='/admin/api')


@admin_api.route('/')
def admin_api_message():
    """
    If the Admin API is running, returns a JSON response.
    """
    return jsonify(admin_api_running=True)  # 200 OK
