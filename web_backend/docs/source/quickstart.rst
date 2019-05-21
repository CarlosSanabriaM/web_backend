Quickstart
==========

Launch the backend in development mode
--------------------------------------

This section explains how to launch the backend server with the REST API in development mode.

Execute the following commands:

::

    cd <project-root-folder>
    # Export the following variables
    export FLASK_APP=web_backend/app.py
    export FLASK_ENV=development
    export FLASK_DEBUG=0

    # Launch the server
    flask run


Deploying the web backend
-------------------------

The instructions for configuring and deploying the flask app are present in the
`'Deploy to Production' section of the Flask documentation <http://flask.pocoo.org/docs/1.0/tutorial/deploy/>`__.
