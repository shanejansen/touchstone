from touchstone.lib.networking.i_network import INetwork


class DockerNetwork(INetwork):
    def __init__(self):
        self.__external_host = 'localhost'
        self.__container_id = None
        self.__port = None
        self.__ui_port = None
        self.__ui_endpoint = ''
        self.__prefix = ''
        self.__endpoint = ''
        self.__username = None
        self.__password = None

    def internal_host(self) -> str:
        return self.__container_id

    def external_host(self) -> str:
        return self.__external_host

    def container_id(self) -> str:
        return self.__container_id

    def set_container_id(self, container_id: str):
        self.__container_id = container_id

    def port(self) -> int:
        return self.__port

    def set_port(self, port: int):
        self.__port = port

    def set_ui_port(self, ui_port: int):
        self.__ui_port = ui_port

    def set_ui_endpoint(self, ui_endpoint: str):
        self.__ui_endpoint = ui_endpoint

    def set_prefix(self, prefix: str):
        self.__prefix = prefix

    def set_endpoint(self, endpoint: str):
        self.__endpoint = endpoint

    def username(self) -> str:
        return self.__username

    def set_username(self, username: str):
        self.__username = username

    def password(self) -> str:
        return self.__password

    def set_password(self, password: str):
        self.__password = password

    def internal_url(self) -> str:
        return f'{self.__prefix + self.__container_id}:{self.__port}{self.__endpoint}'

    def external_url(self) -> str:
        return f'{self.__prefix + self.__external_host}:{self.__port}{self.__endpoint}'

    def ui_url(self) -> str:
        port = self.__ui_port if self.__ui_port else self.__port
        return f'http://{self.__external_host}:{port}{self.__ui_endpoint}'
