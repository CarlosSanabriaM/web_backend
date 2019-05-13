from flask import Blueprint, jsonify

admin_api = Blueprint('admin_api', __name__, url_prefix='/admin/api')


@admin_api.route('/')
def admin_api_message():
    return jsonify(admin_api_running='yes')  # 200 OK
