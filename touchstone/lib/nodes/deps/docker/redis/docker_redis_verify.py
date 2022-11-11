import json

from redis import Redis

from touchstone.helpers import validation
from touchstone.lib.nodes.deps.behaviors.i_redis_behavior import IRedisVerify


class DockerRedisVerify(IRedisVerify):
    def __init__(self):
        self.__redis_client: Redis = None

    def set_redis_client(self, redis_client: Redis):
        self.__redis_client = redis_client

    def value_exists(self, key: str) -> bool:
        return self.__redis_client.get(key) is not None

    def value_matches(self, key: str, value: str) -> bool:
        return self.__redis_client.get(key).decode('utf-8') == value

    def value_matches_json(self, key: str, value: dict) -> bool:
        value_json = json.loads(self.__redis_client.get(key).decode('utf-8'))
        return validation.matches(value, value_json)
