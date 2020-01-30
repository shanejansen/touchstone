import os


def execute():
    if os.path.exists('touchstone/touchstone.yml'):
        print('Touchstone has already been initialized.')
        exit(1)
    os.makedirs('touchstone/defaults')
    os.makedirs('touchstone/tests')
    with open('touchstone/touchstone.yml', 'w', encoding='utf-8') as file:
        data = """---
services:
  - name: my-app
    port: 8080
mocks:
"""
        file.writelines(data)
    open('touchstone/defaults/.gitkeep', 'a').close()
    print('Touchstone has been initialized in the current directory.')
