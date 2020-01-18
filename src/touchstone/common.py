import logging

logger = logging.getLogger('touchstone')


def dict_merge(base: dict, override: dict) -> dict:
    if override is None:
        return base
    return dict(list(base.items()) + list(override.items()))


def replace_host_with_docker_equivalent(host: str) -> str:
    replace = ['localhost', '127.0.0.1', '0.0.0.0']
    for replacement in replace:
        host = host.replace(replacement, 'host.docker.internal')
    return host
