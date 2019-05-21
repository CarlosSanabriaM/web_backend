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

A quick summary for generating the wheel distribution and installing the backend:

::

    cd <project-root-folder>
    # Update/install wheel
    conda install wheel
    # pip install wheel # if using virtualenv instead of conda

    # Create the binary distribution
    python setup.py bdist_wheel

    # Copy this file to another machine, set up a new virtualenv, then install the file with pip.
    # Create the new virtualenv
    virtualenv <env-name>
    # Activate the virtualenv
    source <env-name>/bin/activate
    # (<env-name>) should appear at the beginning of the prompt
    cd <env-name>
    # Install the wheel file
    pip install <path-to-.whl-file>
    # The lib/python3.6/site-packages/web_backend will be created along with other packages

    # Install the topics_and_summary library
    pip install <path-to-topics-and-summary-project-root-folder>

    # Try the flask app
    export FLASK_APP=lib/python3.6/site-packages/web_backend/app.py
    flask run
    # Control + C to stop the development server

    # To leave the virtualenv run:
    deactivate
    # (<env-name>) should disappear form the beginning of the prompt

.. warning:: This doesn't have into account that the files of the topics_and_summary library should be
   located as explained in the :ref:`directory-structure` section.

.. warning:: The development server (the one launched with flask run) is provided for convenience,
   but is not designed to be particularly efficient, stable, or secure. Instead, use a production WSGI server,
   as explained below.


Run with a Production Server
----------------------------

Instead of the development server, a **production WSGI server** must be used in production.

In this case, and for simplicity, we use `Waitress <https://docs.pylonsproject.org/projects/waitress/>`__.

After executing the steps in the previous section, follow this steps:

::

    # Activate the previously created virtualenv
    source <env-name>/bin/activate
    cd <env-name>

    # Install waitress
    pip install waitress

    # Start the server with the web_backend Python module previously installed
    waitress-serve --call 'web_backend:app.py'
