import json
import os

from touchstone import common


def execute():
    if common.sanity_check_passes():
        print('Touchstone has already been initialized.')
        exit(1)
    with open('touchstone.json', 'w', encoding='utf-8') as f:
        data = {
            "services": [
                {
                    "name": "My App",
                    "tests": "tests",
                    "port": 8080
                }
            ],
            "mocks": []
        }
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.makedirs('dev-defaults')
    open('dev-defaults/.gitkeep', 'a').close()
    print('Touchstone has been initialized.')
