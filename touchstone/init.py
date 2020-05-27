import os

from touchstone import __version__


def execute():
    if os.path.exists('touchstone/touchstone.yml'):
        print('Touchstone has already been initialized.')
        exit(1)
    os.makedirs('touchstone/defaults')
    os.makedirs('touchstone/tests')
    open('touchstone/tests/__init__.py', 'a').close()
    with open('touchstone/touchstone.yml', 'w', encoding='utf-8') as file:
        data = f"""---
touchstone-version: {__version__}
services:
  - name: my-app
    port: 8080
mocks:
"""
        file.writelines(data)
    open('touchstone/defaults/.gitkeep', 'a').close()
    print('Touchstone has been initialized in the current directory.')
