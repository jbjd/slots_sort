import os
import re
from collections.abc import Iterator
from pathlib import Path

SLOTS_REGEX: str = r"(?P<start>[ \t]+__slots__[ \t]*=[ \t]*)[\[(](?P<contents>.*?)[\])]"
MAX_LINE_SIZE = 88


def format_as_multiline_string(start_of_string: str, sorted_slot_string: str) -> str:
    """Takes in a one line string of slots and returns it as a multiline string"""

    opening_white_space: str = start_of_string[: start_of_string.find("_")]

    opening_line: str = f"{start_of_string}(\n"
    closing_line: str = f"{opening_white_space})"

    # keep with existing whitespace style
    if "\t" in opening_white_space:
        opening_white_space += "\t"
    else:
        opening_white_space += "    "

    multiline_slot_string: list[str] = [
        f"{opening_white_space}{var}\n" for var in sorted_slot_string.split(" ")
    ]

    sorted_slot_string = "".join(multiline_slot_string)

    return f"{opening_line}{sorted_slot_string}{closing_line}"


def sort_slots(file_contents: str) -> list[str]:
    slots_in_file: Iterator = re.finditer(
        SLOTS_REGEX,
        file_contents,
        re.S,
    )

    replacements: list[str] = []

    for slot in slots_in_file:
        start_of_string: str = slot["start"]
        text: str = slot["contents"]

        text_list: list[str] = sorted(
            [
                clean_string
                for split_string in text.split(",")
                if (clean_string := re.sub(r"\s", "", split_string))
            ]
        )
        sorted_slot_string: str = ", ".join(text_list)

        length_if_one_line: int = len(start_of_string) + len(sorted_slot_string) + 2
        final_string: str
        if length_if_one_line > MAX_LINE_SIZE:
            final_string = format_as_multiline_string(
                start_of_string, sorted_slot_string
            )
        else:
            final_string = f"{start_of_string}({sorted_slot_string})"

        replacements.append(final_string)

    return replacements


def get_updated_file_contents(
    file_contents: str, list_of_replacements: list[str]
) -> str:
    return re.sub(
        SLOTS_REGEX,
        lambda _: list_of_replacements.pop(0),
        file_contents,
        flags=re.S,
    )


def main() -> None:
    working_dir = Path(os.getcwd())

    python_file_paths: list[Path] = [path for path in working_dir.rglob("*.py")]

    for path in python_file_paths:
        with open(path, "r") as fp:
            file_contents: str = fp.read()

        list_of_replacements: list[str] = sort_slots(file_contents)

        if not list_of_replacements:
            continue

        updated_file_contents: str = get_updated_file_contents(
            file_contents, list_of_replacements
        )

        try:
            with open(path, "w") as fp:
                fp.write(updated_file_contents)
        except Exception as e:
            print(f"Warning: Failed to write to file {path}")
            print(e)


main()
