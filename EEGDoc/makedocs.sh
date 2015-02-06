export DJANGO_SETTINGS_MODULE=EEG.settings
rm EEG*.rst
rm modules.rst
sphinx-apidoc -o . ../EEG
python clean-docs.py
make clean
make html
