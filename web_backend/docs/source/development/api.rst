.. _development-api:

Development: API
================

This page explains:

* The `code style`_ used in the library
* The most `important external libraries`_ used in the source code
* The `directory structure and important files`_
* `Important source code details`_
* Tips to `extend the library`_

.. warning:: All the **imports** that refer to modules of the library must specify the **name of the library**:
    ::

        from web_backend.params import get_param, update_param






Dependencies
------------

The instructions for installing the required dependencies are included in the
:ref:`installation-dependencies` section of the *Dependencies and required files* page.





Code style
----------

The code style must follow the :pep:`8` style guide and the **tab size** must be of **4 spaces**.





Important external libraries
----------------------------

Flask
^^^^^

This is the web framework used to implement the backend.

`This is a direct link to the Flask documentation. <http://flask.pocoo.org/docs/1.0/>`__

PyYAML
^^^^^^

This library is used to read and write files in YAML format.

`This is a direct link to PyYAML Flask documentation. <https://pyyaml.org/wiki/PyYAMLDocumentation>`__






Directory structure and important files
---------------------------------------

* **tests** folder: Python package with all the tests of this subsystem.
* **web_backend** folder: Is the python package of the backend. It contains all the source code, and has the following elements:

   * **apis** folder: Python package with functionality of the REST APIS: User API and Admin API (this last one isn't implemented yet).
   * **docs** folder: Contains all the documentation files.
   * **saved-elements** folder: Contains the topics models stored on disk.
   * **static** folder: Contains the wordcloud images.
   * **wrapper** folder: Python package that wraps the functionality of the TopicsModels and SummarizationModels of the topics_and_summary library.
   * **app.py**: Python module that creates the Flask app.
   * **utils.py**: Python module with some utilities: paths, rename attributes, access to the x-conf.ini params and User Defined Exceptions.
   * **params.py**: Python module that encapsulates the access to the params-file.yaml file with the system parameters.
   * **params-file.yaml**: File that contains the system parameters.
   * **user-api-swagger.yaml**: File that contains the OpenAPI Specification (Swagger Specification) of the User REST API.

* **development-conf.ini**: Configuration file for the development environment that stores, among other things, the paths to the required files explained in the note below.
* **production-conf.ini**: Configuration file for the production environment that stores, among other things, the paths to the required files explained in the note below.
* **generate-requirements.sh**: Creates the requirements.txt file based on the libraries used in the source code.
* **requirements.txt**: Required dependencies.
* **setup.py**: File used to install the library or generate the binary distribution. It contains information about the library installation.
* **sonar-project.properties**: Contains the configuration for the SonarQube static code analysis tool.
* **Dockerfile**: Contains the steps for creating the docker image to run the backend.
* **.dockerignore**: Contains the files and folders ignored by the docker build context. Those files are not copied to the docker image.
* **mallet-docker**: Shell script used to communicate with the Java mallet library, with some memory configurations for Docker.
  This file will replace the mallet-2.0.8/bin/mallet file while creating the Docker image.
* **.gitignore**: Contains the files and folders ignored by git.
* **MANIFEST.in**: Define the list of files to include in the package installation.
* **README.md**: Contains a quick explanation of the project.


.. note:: The are some other files needed to use the library, and they are explained in the
   :ref:`required-directories-files` section of the *Dependencies and required files* page.

.. note:: For more information about the OpenAPI Specification, visit the following link:
   `https://swagger.io/docs/specification/about/ <https://swagger.io/docs/specification/about/>`__.






Important source code details
-----------------------------

CONF_INI_FILE_PATH environment variable
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

**CONF_INI_FILE_PATH is an environment variable that must be set to be able to execute the application
or generate the documentation.** In development, it's value must be the absolute path to the development-conf.ini file.

The development-conf.ini file contains some configuration used in the development, for example, paths to the models.

On **PyCharm**, this variable can be set in: Run --> Edit Configurations... --> + (Add new configuration) --> Flask Server -->
Configuration tab --> Environment section --> Environment variables.

To set the variable in the Unix or MacOS terminal execute:

   ::

      export CONF_INI_FILE_PATH=<path/to/development-conf.ini>

To set the variable in Windows CMD execute:

   ::

      set CONF_INI_FILE_PATH=<path/to/development-conf.ini>


Flask Blueprints
^^^^^^^^^^^^^^^^

The user and the admin REST APIs are implemented using Flask Blueprints. This allows to, among other things,
have independent url_prefix in each Blueprint.

.. note:: For more information about the OpenAPI Specification, visit the following link:
   `http://flask.pocoo.org/docs/1.0/blueprints/ <http://flask.pocoo.org/docs/1.0/blueprints/>`__.







Extend the library
------------------

This section gives information about how to extend the library functionality.

Recommended IDE
^^^^^^^^^^^^^^^

The recommended IDE is `Pycharm <https://www.jetbrains.com/pycharm/>`__. The folder to be selected as a project must be
the project root folder (web_backend, not web_backend/web_backend).

Static Code Analysis with SonarQube
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Start the SonarQube server
""""""""""""""""""""""""""

SonarQube server must be installed. See the `SonarQube downloads page <https://www.sonarqube.org/downloads/>`__.

See also the `Get Started in Two Minutes Guide <https://docs.sonarqube.org/latest/setup/get-started-2-minutes/>`__.


On Windows, execute:

::

   C:\<path>\sonarqube\bin\windows-x86-xx\StartSonar.bat

On other operating systems, as a non-root user execute:

::

   <path>/sonarqube/bin/<OS>/sonar.sh console

Launch the SonarQube scanner
""""""""""""""""""""""""""""

SonarQube scanner must be installed. See the `SonarQube scanner page <https://docs.sonarqube.org/display/SCAN/Analyzing+with+SonarQube+Scanner>`__.

The SonarQube server must be running.

After adding the <install_directory>/bin directory to your path, execute the following command:

::

   cd <project-root-path>
   sonar-scanner

After that, open the browser in `localhost:9000 <localhost:9000>`__ to see the results.