ANY = object()


def __equals(expected, actual) -> bool:
    if expected == ANY:
        return True
    return expected == actual


def __equals_list(expected: list, actual: list) -> bool:
    if len(expected) != len(actual):
        return False
    for expected_item in expected:
        expected_item_in_actual = False
        for actual_item in actual:
            if matches(expected_item, actual_item, quiet = True):
                expected_item_in_actual = True
                break
        if not expected_item_in_actual:
            return False
    return True


def __equals_dict(expected: dict, actual: dict) -> bool:
    if len(expected) != len(actual):
        return False
    for k, v in expected.items():
        if k not in actual:
            return False
        if not matches(v, actual[k], quiet = True):
            return False
    return True


def matches(expected, actual, quiet: bool = False) -> bool:
    if isinstance(expected, dict) and isinstance(actual, dict):
        result = __equals_dict(expected, actual)
    elif isinstance(expected, list) and isinstance(actual, list):
        result = __equals_list(expected, actual)
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
