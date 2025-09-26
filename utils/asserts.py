class Asserts:
    @staticmethod
    def assert_equal(expected: int, actual: int):
        assert expected == actual, f"The balance values differ: expected: {expected}, actual: {actual}"
