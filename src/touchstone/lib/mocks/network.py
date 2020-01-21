class Network(object):
    def __init__(self, host: str, port: int, prefix: str = '', endpoint: str = '', ui_port: int = None,
                 ui_endpoint: str = ''):
        self.host = host
        self.port = port
        self.prefix = prefix
        self.endpoint = endpoint
        self.ui_port = ui_port
        self.ui_endpoint = ui_endpoint

        if not self.ui_port:
            self.ui_port = self.port

    def url(self) -> str:
        return f'{self.prefix + self.host}:{self.port}{self.endpoint}'

    def ui_url(self):
        return f'http://{self.host}:{self.ui_port}{self.ui_endpoint}'
