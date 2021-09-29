from os import path

from setuptools import setup, find_packages

this_directory_abs_path = path.abspath(path.dirname(__file__))
with open(path.join(this_directory_abs_path, 'README.md'), "r") as fh:
    long_description = fh.read()

setup(name='web_backend',
      version='1.0',
      description='Web backend for the topics_and_summary library',
      long_description=long_description,
      long_description_content_type="text/markdown",
      keywords="web backend topics_and_summary topics summary rest api flask",

      url='https://github.com/CarlosSanabriaM/web_backend',
      project_urls={
          "Source Code": "https://github.com/CarlosSanabriaM/web_backend",
          "Documentation": "https://github.com/CarlosSanabriaM/web_backend/web_backend/docs"
      },

      author='Carlos Sanabria Miranda',
      author_email='uo250707@uniovi.es',

      install_requires=[
          'typing==3.6.6',
          'tqdm==4.31.1',
          'Werkzeug==0.15.2',
          'networkx==2.2',
          'Flask==1.0.2',
          'Flask-Cors==3.0.7',
          'nltk==3.6.3',
          'PyYAML==5.1',
      ],
      packages=find_packages(),
      include_package_data=True,
      zip_safe=False)
