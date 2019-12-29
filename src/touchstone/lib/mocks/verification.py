def expected_matches_actual(expected, actual) -> bool:
    if expected == actual:
        return True
    print(f'Expected "{expected}" does not match actual "{actual}".')
    return False


def expected_in_actual(expected, actual) -> bool:
    if expected in actual:
        return True
    print(f'Expected "{expected}" was not found in actual "{actual}".')
    return False
