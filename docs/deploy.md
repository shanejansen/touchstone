```commandline
# Create dist
python setup.py sdist bdist_wheel

# Ensure Twine is installed
python -m pip install --upgrade twine

# Upload to test PyPi (remove --repository-url for prod PyPi)
python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*

# Upgrade version
pip install --upgrade touchstone-testing

# Upgrade version from test PyPi
pip install -i https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple touchstone-testing==x.x.x
```
