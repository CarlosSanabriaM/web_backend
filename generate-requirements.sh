#!/bin/sh

# Add the packages used in the project (only includes packages imported in .py files of external packages)
pipreqs web_backend --force --savepath requirements.txt
# More info in https://github.com/bndr/pipreqs

# Change all the '_' in the name of the packages by '-', because packages are installed using '-' instead of '_'
# For example, 'scikit_learn' is installed as 'scikit-learn'
sed -i'.original' -e 's/_/-/g' requirements.txt
# Remove *.original files generated as backup by sed
rm *.original