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
            if not __equals_dict(v, actual[k]):
                return False
        elif not __equals(v, actual[k]):
            return False
    return True


def matches(expected, actual, quiet: bool = False) -> bool:
    if isinstance(expected, dict) and isinstance(actual, dict):
        result = __equals_dict(expected, actual)
    else:
        result = __equals(expected, actual)
    if not result and not quiet:
        print(f'Expected:\n{expected}\ndoes not match actual:\n{actual}')
    return result


def contains(expected, actual, quiet: bool = False) -> bool:
    if expected in actual:
        return True
    if not quiet:
        print(f'Expected:\n{expected}\nwas not found in actual:\n{actual}')
    return False
