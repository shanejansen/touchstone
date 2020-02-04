class Network(object):
    def __init__(self, network_host: str, port: int, network_port: int, prefix: str = '', endpoint: str = '',
                 ui_port: int = None, ui_endpoint: str = '', host: str = None):
        self.host = host
        self.network_host = network_host
        self.port = port
        self.network_port = network_port
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

    def network_url(self):
        return f'{self.prefix + self.network_host}:{self.network_port}{self.endpoint}'
