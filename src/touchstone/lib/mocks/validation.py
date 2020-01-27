ANY = 'TS_ANY'


def __equals(expected, actual) -> bool:
    if expected == ANY:
        return True
    return expected == actual


def __equals_dict(expected: dict, actual: dict) -> bool:
    for k, v in d.items():
        if isinstance(v, dict):
            __equals_dict()
        else:
            __equals()


def expected_matches_actual(expected, actual) -> bool:
    if isinstance(expected, str) and isinstance(actual, str):
        return __equals(expected, actual)
    if isinstance(expected, dir) and isinstance(actual, dir):


# result = False
# if expected == actual:
#     return True
# print(f'Expected "{expected}" does not match actual "{actual}".')
# return False


def expected_in_actual(expected, actual) -> bool:
    if expected in actual:
        return True
    print(f'Expected "{expected}" was not found in actual "{actual}".')
    return False
