from sys import argv
from typing import Any, Callable


def _validate_args(args: list[str]) -> int:
    if len(args) > 1:
        raise ValueError("The number of arguments > 1")
    nbr: str = (args[0]).strip() if args else "0"
    if not nbr.isdigit():
        raise TypeError(f"The {nbr} is not digits-only.")
    return int(nbr)


def _default_hash_validator(hash_: str) -> bool:
    if (len(hash_) == 32) and hash_.startswith("00000") and hash_[5] != "0":
        return True
    return False


def main(
    num_of_lines: int, hash_validator: Callable[[str], Any] = _default_hash_validator
):
    """The main entry point."""

    try:
        for _ in range(num_of_lines):
            hash_ = input()
            if hash_validator(hash_):
                print(hash_)
    except EOFError:
        pass


if __name__ == "__main__":
    try:
        nlines = _validate_args(argv[1:])
        main(nlines)
    except Exception as err:
        print(f"Error: {err}")