import os


class Config(object):
    def __init__(self):
        self.vars = {
            'db_host': os.getenv('TS_MYSQL_HOST', 'localhost'),
            'db_port': os.getenv('TS_MYSQL_PORT', '3306'),
            'db_username': os.getenv('TS_MYSQL_USERNAME', 'root'),
            'db_password': os.getenv('TS_MYSQL_PASSWORD', 'root')
        }
