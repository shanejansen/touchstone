class Network(object):
    def __init__(self, internal_host: str, internal_port: int, external_port: int, ui_port: int = None,
                 ui_endpoint: str = '', prefix: str = '', endpoint: str = '', external_host: str = None, username=None,
                 password=None):
        self.internal_host = internal_host
        self.external_host = external_host
        self.internal_port = internal_port
        self.external_port = external_port
        self.ui_port = ui_port
        self.ui_endpoint = ui_endpoint
        self.prefix = prefix
        self.endpoint = endpoint
        self.username = username
        self.password = password

        if not self.ui_port:
            self.ui_port = self.external_port

    def internal_url(self):
        return f'{self.prefix + self.internal_host}:{self.internal_port}{self.endpoint}'

    def external_url(self) -> str:
        return f'{self.prefix + self.external_host}:{self.external_port}{self.endpoint}'

    def ui_url(self):
        return f'http://{self.external_host}:{self.ui_port}{self.ui_endpoint}'
