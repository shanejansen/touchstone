import json
import os


def execute():
    if os.path.exists('touchstone/touchstone.json'):
        print('Touchstone has already been initialized.')
        exit(1)
    os.makedirs('touchstone/defaults')
    os.makedirs('touchstone/tests')
    with open('touchstone/touchstone.json', 'w', encoding='utf-8') as f:
        data = {
            "services": [
                {
                    "name": "My App",
                    "tests": "./tests",
                    "port": 8080
                }
            ],
            "mocks": []
        }
        json.dump(data, f, ensure_ascii=False, indent=2)
    open('touchstone/defaults/.gitkeep', 'a').close()
    print('Touchstone has been initialized.')
