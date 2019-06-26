Execution and Deployment
========================

Launch in development mode
--------------------------

This section explains how to launch the backend server with the REST API in development mode.

Execute the following commands:

::

    cd <project-root-folder>
    # Export the following variables
    export FLASK_APP=web_backend/app.py
    export FLASK_ENV=development
    export FLASK_DEBUG=0
    export CONF_INI_FILE_PATH=<path/to/development-conf.ini>  # Path to the development configuration file

    # Launch the server
    flask run


Instructions for generic deployment
-----------------------------------

The instructions for configuring and deploying the flask app are present in the
`'Deploy to Production' section of the Flask documentation <http://flask.pocoo.org/docs/1.0/tutorial/deploy/>`__.

A quick summary for generating the wheel distribution and installing the backend and the topics_and_summary library
in a isolated virtualenv:

::

    cd <project-root-folder>
    # Update/install wheel
    conda install wheel
    # pip install wheel # if using virtualenv instead of conda

    # Create the binary distribution of the web_backend
    python setup.py bdist_wheel

    # Copy this file to another machine, set up a new virtualenv, then install the file with pip.
    # Create the new virtualenv
    virtualenv <env-name>
    # Activate the virtualenv
    source <env-name>/bin/activate
    # (<env-name>) should appear at the beginning of the prompt
    cd <env-name>
    # Install the wheel file with the backend
    pip install <path-to-.whl-file>
    # The lib/python3.6/site-packages/web_backend will be created along with other packages

    # Install the topics_and_summary library
    # Create the binary distribution of the topics_and_summary library
    python <path-to-topics-and-summary-project-root-folder>/setup.py bdist_wheel
    # Install the wheel file with the topics_and_summary library
    pip install <path-to-.whl-file-of-topics-and-summary-project>
    # Install nltk resources
    python -c "import nltk;nltk.download('stopwords');nltk.download('wordnet');nltk.download('punkt')"

    # Try the flask app
    export CONF_INI_FILE_PATH=<path/to/production-conf.ini>  # Path to the production configuration file
    export FLASK_APP=<env-path>/lib/python3.6/site-packages/web_backend/app.py
    flask run
    # Control + C to stop the development server

    # To leave the virtualenv run:
    deactivate
    # (<env-name>) should disappear form the beginning of the prompt

.. warning:: The paths to some directories/files must be specified in the x-conf.ini file.
   This files are explained in the :ref:`required-directories-files` section.

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

    # Export the configuration file variable
    export CONF_INI_FILE_PATH=<path/to/production-conf.ini>  # Path to the production configuration file

    # Start the server with the web_backend Python module previously installed
    # The server listens in the 8080 port
    waitress-serve --port=8080 --host='0.0.0.0' --call web_backend.app:create_app


Generate and run a docker image
-------------------------------

The Dockerfile included in the web_backend root directory can be used to generate a docker image.

.. warning:: The Dockerfile and the .dockerignore files are included in the web_backend root directory **only
   for version control reasons**. **This 2 files must be moved to the parent directory of the web_backend root directory**.,
   The topics_and_summary root directory also must be at the same level, i.e.:

    .

    ├── .dockerignore

    ├── Dockerfile

    ├── topics_and_summary

    └── web_backend

To generate the docker image, execute the following commands:

::

    # Move to the folder that contains the Dockerfile, and the web_backend and topics_and_summary folder
    cd <web-backend-root-directory-parent-folder>
    # Build the docker image (executes the Dockerfile)
    docker build . -t web_backend:latest
    # . is the build context. In this case, the current directory
    # -t web_backend:latest specifies the name=web_backend and tag=latest for the image

To create a docker container using the previously created image and run it, execute:

::

    # Create a container that executes the web backend at startup and lets it be accessible via the <host-port> port of the host
    docker run --name web_backend -p <host-port>:8080 -e PORT=8080 -i -t web_backend:latest
    # --name web_backend specifies the name of the container
    # -p <host-port>:8080 specifies that the host port specified by the user will be mapped to the port 8080 of the container
    # -e PORT=8080 sets the value of the $PORT environment variable used inside the Dockerfile.
    # This value must be the same as the one specified in the second value of the -p argument, and must be > than 1024. Recommended is 8080
    # -i and -t are used for interactive mode
    # web_backend:latest specifies name:tag of the image that will be used to create the container

    ### ALTERNATIVE WAY OF CREATING THE CONTAINER TO ENTER INSIDE IT ###
    # Create a container and enter inside it, using a bash shell
    docker run --name web_backend -p <host-port>:8080 -e PORT=8080 -i -t web_backend:latest /bin/bash
    # The command is the same, except the last instruction: '/bin/bash'
    # This overrides the default CMD command executed by the docker container at startup, executing a bash shell
    # The default command is: waitress-serve --port=$PORT --host='0.0.0.0' --call web_backend.app:create_app
    # This command starts the backend in the port specified by the environment variable PORT

With this container running, the web backend will be accessible via the <host-port> port of the host machine.


Deploy to Heroku
----------------

The web backend is deployed in Heroku in the following url: https://topics-and-summary-web-backend.herokuapp.com/.

This was done creating an Heroku app called **topics-and-summary-web-backend**.

The docker image created in the previous section is used to deploy the backend to Heroku. This is done using the
`Heroku CLI <https://devcenter.heroku.com/articles/heroku-cli>`__. The commands are:

::

    # Log in to Heroku
    heroku login
    # Enter credentials

    # Log in to Container Registry
    heroku container:login
    # 'Login Succeeded' message must appear

    # Create a tag registry.heroku.com/topics-and-summary-web-backend/web that refers to web_backend image
    docker tag web_backend registry.heroku.com/topics-and-summary-web-backend/web

    # Push the image to the heroku docker registry
    docker push registry.heroku.com/topics-and-summary-web-backend/web

    # Release the web backend application
    heroku container:release web --app topics-and-summary-web-backend
