from slots_sort.main import get_updated_file_contents, sort_slots


def test_single_line_slots():
    example_input: str = """
class A:
    __slots__ = ["asdf"]
"""
    expected_output: str = """
class A:
    __slots__ = ("asdf")
"""
    formated_slots: str = sort_slots(example_input, 88)
    assert formated_slots[0] == '    __slots__ = ("asdf")'

    output: str = get_updated_file_contents(example_input, formated_slots)

    assert output == expected_output


def test_long_line_slots():
    example_input: str = """
class A:
    __slots__ = ["asdf", "zasdf", "abghjkl", "asdf1234"]
"""
    expected_output: str = """
class A:
    __slots__ = (
        "abghjkl",
        "asdf",
        "asdf1234",
        "zasdf",
    )
"""
    # set max line length to small numer
    formated_slots: str = sort_slots(example_input, max_line_length=10)
    output: str = get_updated_file_contents(example_input, formated_slots)

    assert output == expected_output

    # Also test with a single item in brackets thats too long
    example_input = """
class A:
    __slots__ = ["asdf"]
"""
    expected_output = """
class A:
    __slots__ = (
        "asdf",
    )
"""
    # set max line length to small numer
    formated_slots: str = sort_slots(example_input, max_line_length=10)
    output: str = get_updated_file_contents(example_input, formated_slots)

    assert output == expected_output


def test_multiple_classes_slots():
    example_input: str = """
class A:
    __slots__ = ["asdf", "zasdf", "abghjkl", "asdf1234"]

    class B:

        __slots__ = ["asdf"]

        def __init__(self):
            pass
"""
    expected_output: str = """
class A:
    __slots__ = (
        "abghjkl",
        "asdf",
        "asdf1234",
        "zasdf",
    )

    class B:

        __slots__ = ("asdf")

        def __init__(self):
            pass
"""
    # set max line so only class A becomes multiline
    formated_slots: str = sort_slots(example_input, max_line_length=40)
    output: str = get_updated_file_contents(example_input, formated_slots)

    assert output == expected_output
