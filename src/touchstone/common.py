import logging
import os

logger = logging.getLogger('touchstone')


def sanity_check_passes() -> bool:
    touchstone_path = os.path.join(os.getcwd(), 'touchstone.yml')
    defaults_path = os.path.join(os.getcwd(), 'defaults')
    return os.path.exists(touchstone_path) and os.path.exists(defaults_path)


def prep_run():
    if not sanity_check_passes():
        print('touchstone.yml and the defaults directory could not be found. '
              'If touchstone has not been initialized, run \'touchstone init\'.')
        exit(1)


def dict_merge(base: dict, override: dict) -> dict:
    if override is None:
        return base
    return dict(list(base.items()) + list(override.items()))


def replace_host_with_docker_equivalent(host: str) -> str:
    replace = ['localhost', '127.0.0.1', '0.0.0.0']
    for replacement in replace:
        host = host.replace(replacement, 'host.docker.internal')
    return host
