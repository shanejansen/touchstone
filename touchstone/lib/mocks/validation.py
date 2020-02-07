ANY = 'TS_ANY'


def __equals(expected, actual) -> bool:
    if expected == ANY:
        return True
    return expected == actual


def __equals_dict(expected: dict, actual: dict) -> bool:
    if len(expected) != len(actual):
        return False
    for k, v in expected.items():
        if k not in actual:
            return False
        if isinstance(v, dict):
            return __equals_dict(v, actual[k])
        if not __equals(v, actual[k]):
            return False
    return True


def matches(expected, actual) -> bool:
    if isinstance(expected, dict) and isinstance(actual, dict):
        result = __equals_dict(expected, actual)
    else:
        result = __equals(expected, actual)
    if not result:
        print(f'Expected "{expected}" does not match actual "{actual}".')
    return result


def contains(expected, actual) -> bool:
    if expected in actual:
        return True
    print(f'Expected "{expected}" was not found in actual "{actual}".')
    return False
