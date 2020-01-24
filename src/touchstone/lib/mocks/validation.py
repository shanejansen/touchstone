ANY = 'TS_ANY'


def __string(expected: str, actual: str) -> bool:
    return expected == actual


def expected_matches_actual(expected, actual) -> bool:
    result = False
    if expected == actual:
        return True
    print(f'Expected "{expected}" does not match actual "{actual}".')
    return False


def expected_in_actual(expected, actual) -> bool:
    if expected in actual:
        return True
    print(f'Expected "{expected}" was not found in actual "{actual}".')
    return False
