from flask import Flask

from web_backend.apis.admin import admin_api
from web_backend.apis.user import user_api

app = Flask(__name__)
app.register_blueprint(user_api)
app.register_blueprint(admin_api)


@app.route('/')
def app_running_message():
    return 'Web backend is running'


if __name__ == '__main__':
    app.run()
