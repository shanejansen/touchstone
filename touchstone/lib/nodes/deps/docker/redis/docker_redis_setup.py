from redis import Redis

from touchstone.lib import exceptions
from touchstone.lib.nodes.deps.behaviors.i_redis_behavior import IRedisSetup


class DockerRedisSetup(IRedisSetup):
    def __init__(self):
        self.__redis_client: Redis = None

    def set_redis_client(self, redis_client: Redis):
        self.__redis_client = redis_client

    def init(self, defaults: dict):
        self.__redis_client.flushall()
        for key, value in defaults.get('objects', []).items():
            self.__redis_client.set(key, value)

    def set(self, key: str, value: str):
        if not isinstance(value, str):
            raise exceptions.DepException('Value must be a str.')
        return self.__redis_client.set(key, value)
