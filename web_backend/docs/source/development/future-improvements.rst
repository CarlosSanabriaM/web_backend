Future Improvements
===================

Source code
-----------

* Implement the **admin REST API**: This API must allow the admin to access the system params (the ones stored in the
  params-file.yaml file, which are used to limit the values that can introduce the users in the User REST API).
  The API must have authentication and must be implemented in the web_backend.apis.user.py module.
  This API allows the admin to get the value of the params and modify them.



Documentation
-------------

* Change the **API packages and modules toctree** to don't show *web_backend package* as a first item.
* Generate the documentation of each Python module or class in the same way as pandas library documentation does.
  As an example, check the `pandas Series class documentation <https://pandas.pydata.org/pandas-docs/stable/reference/series.html>`__.
  This is done with the \.. autosummary:: directive. The source code of the pandas Series class documentation
  is available on `this GitHub page <https://raw.githubusercontent.com/pandas-dev/pandas/master/doc/source/reference/series.rst>`__.
* Create equivalent .bat files for the existing .sh files used for generating the api documentation.
* Create equivalent .bat files for the existing .sh files used for generating the requirements files.
