from flask import Blueprint

admin_api = Blueprint('admin_api', __name__, url_prefix='/admin/api')


@admin_api.route('/')
def admin_api_message():
    return 'Admin API'
