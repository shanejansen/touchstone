import os

from touchstone import __version__


def execute():
    if os.path.exists(os.path.join('touchstone', 'touchstone.yml')):
        print('Touchstone has already been initialized.')
        exit(1)
    os.makedirs(os.path.join('touchstone', 'defaults'))
    os.makedirs(os.path.join('touchstone', 'tests'))
    open(os.path.join('touchstone', 'tests', '__init__.py'), 'a').close()
    with open(os.path.join('touchstone', 'touchstone.yml'), 'w', encoding='utf-8') as file:
        data = f"""---
touchstone_version: {__version__}
services:
  - name: my-app
    port: 8080
mocks:
"""
        file.writelines(data)
    open(os.path.join('touchstone', 'defaults', '.gitkeep'), 'a').close()
    print('Touchstone has been initialized in the current directory.')
