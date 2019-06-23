from flask import Flask, jsonify
from flask_cors import CORS
from werkzeug.exceptions import HTTPException


def create_app():
    """
    Application Factory function. \
    See http://flask.pocoo.org/docs/1.0/tutorial/factory/ for more information.

    :return: The Flask application.
    """
    # Create and configure the app
    # The app needs to know where it’s located to set up some paths,
    # and __name__ is a convenient way to tell it that.
    app = Flask(__name__)

    # Allow CORS for all domains on all routes
    CORS(app)

    # Register blueprints of the user and admin apis
    from web_backend.apis.user import user_api
    app.register_blueprint(user_api)

    from web_backend.apis.admin import admin_api
    app.register_blueprint(admin_api)

    # Create a route to check if the application is running
    @app.route('/')
    def app_running_message():
        res = jsonify(web_backend_running=True)
        res.status_code = 200
        return res

    # Create and error handler
    @app.errorhandler(HTTPException)
    def bad_request(error=None):  # error param is obligatory
        """
        Error handler for all HTTPExceptions.

        This function is called by Flask when a HTTPException is raised. This type of exception can be raised
        by Flask automatically in some situations, or can be raised by the user in the following 2 ways:

        * raise <HTTPException>, where <HTTPException> is a subclass of werkzeug.exceptions.HTTPException
        * **abort(<status_code>, description='Error description message')**, where <status_code> is a HTTP status code

        **The second form is preferred.** In the second form, the description param is optional. If it's not given,
        the description value will be a default description of the HTTP status_code provided.

        The handler returns the following info in JSON format:

        * **status_code:** For example: 400
        * **status_name:** For example: 'Bad Request'
        * **description:** For example: 'The browser (or proxy) sent a request that this server could not understand.'
        """
        message = {
            'status_code': error.code,
            'status_name': error.name,
            'description': error.description
        }
        return jsonify(message), error.code

    return app


if __name__ == '__main__':
    app = create_app()
    app.run()
