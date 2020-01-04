import logging

logger = logging.getLogger('touchstone')


def dict_merge(base: dict, override: dict) -> dict:
    if override is None:
        return base
    return dict(list(base.items()) + list(override.items()))
