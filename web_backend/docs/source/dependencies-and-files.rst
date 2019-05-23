.. _dependencies-and-required-files:

Dependencies and required files
===============================

.. _installation-dependencies:


Dependencies
------------

The dependencies are listed in the **requirements.txt** file, which content is showed below:

.. include:: ../../../requirements.txt
   :literal:

.. warning:: There is another dependency not mentioned here, the topics_and_summary library.
   This library is the main subsystem, and **it's not uploaded to any Python package repository**,
   so all it's source code and files must't be present as explained in the Usage Installation section of the
   topics_and_summary library documentation. This library must be installed manually with pip, as explained
   in the :ref:`installation-topics-and-summary` section.


The other dependencies can be installed using `pip <https://pypi.org/project/pip/>`__ or `conda <https://conda.io>`__.

The packages should be installed into an **environment**,
using either `virtualenv <https://virtualenv.pypa.io/en/latest/>`__
or `conda environments <https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__,
but conda is preferred.


Install dependencies using pip
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In a new virtualenv
"""""""""""""""""""
::

    # Create the new virtualenv
    virtualenv <env-name>

    # Activate the virtualenv
    source <env-name>/bin/activate
    # (<env-name>) should appear at the beginning of the prompt

    # Install the required packages to use the library
    pip install -r <path-to-project-root-folder>/requirements.txt
    # Packages will be installed in the <env-name> folder, avoiding conflicts with other projects


::

    # To leave the virtualenv run:
    deactivate
    # (<env-name>) should disappear form the beginning of the prompt

Install dependencies using conda
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
In a new conda environment
""""""""""""""""""""""""""
::

    # Create the environment with the packages needed to use the library
    conda create --name=<environment-name> --file=<path-to-project-root-folder>/requirements.txt --channel conda-forge
    # Packages will be installed in the <environment-name> environment, avoiding conflicts with other environments

    # Change the current conda environment to the new environment
    conda activate <environment-name>
    # (<environment-name>) should appear at the beginning of the prompt, instead of (base)

::

    # To leave the conda environment run:
    conda deactivate
    # (base) should appear at the beginning of the prompt, instead of (<environment-name>)

In an existing conda environment
""""""""""""""""""""""""""""""""
::

    # Change the current conda environment to the existing environment
    conda activate <environment-name>
    # (<environment-name>) should appear at the beginning of the prompt, instead of (base)

    # Install the required packages to use the library
    conda install --file=<path-to-project-root-folder>/requirements.txt --channel conda-forge
    # Packages will be installed in the <environment-name> environment, avoiding conflicts with other environments

::

    # To leave the conda environment run:
    conda deactivate
    # (base) should appear at the beginning of the prompt, instead of (<environment-name>)


.. _installation-topics-and-summary:

Install the topics_and_summary library
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Execute the following command inside the venv or conda environment:

::

    # Create the binary distribution of the topics_and_summary library
    python <path-to-topics-and-summary-project-root-folder>/setup.py bdist_wheel
    # Install the wheel file with the topics_and_summary library
    pip install <path-to-.whl-file-of-topics-and-summary-project>

To check if everything was installed correctly, execute the following commands:

::

    python
    >>> from topics_and_summary.datasets.twenty_news_groups import TwentyNewsGroupsDataset
    >>> dataset = TwentyNewsGroupsDataset()
    >>> dataset.print_some_files()
    # It should print some files of the dataset


.. _required-directories-files:

Required directories/files
--------------------------

This section explains the required directories/files for executing the topics_and_summary library functionality correctly.

.. note:: This info is explained in more detail in the *Download other elements* section of the *Usage Installation* page
   of the topics_and_summary library documentation.

* **20_newsgroups** folder: Contains the 20_newsgroups dataset.
* **glove.6B** folder: Contains the Glove word embeddings.
* **GoogleNews-vectors-negative300.bin.gz**: Contains the Word2Vec word embeddings.
* **mallet-2.0.8** folder: Is the mallet source code folder, obtained after decompressing the mallet-2.0.8.tar.gz file.

.. warning:: Absolute paths to all this folders must be specified in the **conf.ini** configuration file.
