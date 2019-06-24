# Web backend 

## What is it?
This project is a Flask application that represents the web backend of my final degree project.

This application serves a REST API that wraps the functionality of the **topics_and_summary** library.

This REST API is consumed by the [web-frontend](https://github.com/CarlosSanabriaM/web-frontend), but can
also be consumed by other applications.

It's deployed in Heroku in the following URL: 
[https://topics-and-summary-web-backend.herokuapp.com](https://topics-and-summary-web-backend.herokuapp.com).

A Swagger documentation of the User REST API is present in the following URL: 
[https://app.swaggerhub.com/apis-docs/CarlosSanabriaM/topics_and_summary/1.0](https://app.swaggerhub.com/apis-docs/CarlosSanabriaM/topics_and_summary/1.0).



## Main features
* **Uses Flask Blueprints to separate the user API and the admin API.** The admin API is not yet implemented.
* **Uses YAML format for the business application parameters.**
* **Uses ini format for the configuration parameters.**
* **Uses Sphinx for generating the documentation.**
* **Uses Swagger to document the User REST API (user-api-swagger.yaml).**
* **Contains a Postman collection file to easily test the User REST API (web_backend.postman_collection.json)**. 
  This file must be specified in the Postman import option.
* **Uses setuptools to generate a binary distribution of the python package and install the application**



## Dependencies, Installation and Usage
All this information and more is present in the **documentation**.

To generate the documentation and visualize it, modify the paths in the `development-conf.ini` file to point 
to the actual location of the files, and then, execute:

```bash
cd <project-root-folder>/web_backend/docs

# Set the environment variable CONF_INI_FILE_PATH to point to the absolute path of the development-conf.ini file
# In Linux or MacOS:
export CONF_INI_FILE_PATH=<path/to/development-conf.ini>
# In Windows:
set CONF_INI_FILE_PATH=<path/to/development-conf.ini>

# Generate the documentation
./generate-api-doc.sh
```

After that, a <project-root-folder>/web_backend/docs/build/html folder will be generated.

Open the index.html file inside that folder with a browser to visualize the documentation.
