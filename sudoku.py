from pathlib import Path
from collections import Counter
from itertools import repeat


Sudoku = list[list[int]]

def load_sudoku(file_path: Path) -> Sudoku:
    """Parse sudoku from file. Empty cells ('0' or 'x') are denoted by a 0.

    Raises:
        FileNotFoundError: The filename provided has not been found.
        PermissionError: The program has no read access to the file.
    """
    sudoku = []
    raw_lines = file_path.read_text(encoding="utf-8").splitlines()

    for i, line in enumerate(raw_lines):
        try:
            # filter irrelevent symbols
            line = filter(lambda c: "0" <= c <= "9" or c == "x", line.strip())
            # convert the remaining chars of the line to integers
            line = list(map(lambda c: 0 if c=="x" else int(c), line))
            if len(line):
                sudoku.append(line)
        except ValueError as e:
            raise ValueError(f"Line {i+1} has elements that cannot be converted to int.") from e

    assert_sudoku_valid(sudoku)
    return sudoku


def display(s: Sudoku, file=None) -> None:
    """Display a Sudoku. A stream can be provided. Default output to the console."""
    # source unicode chars: https://en.wikipedia.org/wiki/List_of_Unicode_characters#Box_Drawing

    raw_lines = []

    for i, line in enumerate(s, start=1):
        str_ = ""
        for j, cell in enumerate(line, start=1):
            # convert cell value to string
            str_ += "   " if cell == 0 else f" {cell} "
            # draw vertical separator
            str_ += "" if j == 9 else "║" if j in (3, 6) else "│"
        raw_lines.append(str_)
        if i != 9:
            # draw horizontal separator
            sep         = "═" if i in (3, 6) else "─"
            small_cross = "╪" if i in (3, 6) else "┼"
            large_cross = "╬" if i in (3, 6) else "╫"
            raw_lines.append(
                large_cross.join(repeat(small_cross.join(repeat(sep*3, 3)), 3))
            )
    print(*raw_lines, sep="\n", file=file)


def assert_sudoku_valid(s: Sudoku) -> None:
    """Check whether the given sudoku is valid. Unknow cells are denoted by 0."""

    assert len(s) == 9, f"The game has {len(s)} lignes instead of 9."
    assert set(len(line) for line in s) == {9}, "The game has lines with less or more than 9 cells."

    # check lignes
    for line in range(9):
        assert is_unique(s[line]), f"Line {line + 1} is not valid."

    # check columns
    for col in range(9):
        colonne = [s[line][col] for line in range(9)]
        assert is_unique(colonne), f"Column {col + 1} is not valid."

    # check chunks
    for line in range(3):
        for col in range(3):
            chunk = [cell for i in range(3) for cell in s[line * 3 + i][col * 3:(col + 1) * 3]]
            assert  is_unique(chunk), f"Chunk ({line+1}, {col+1}) is not valid."


def is_unique(line: list[int]) -> bool:
    """Check whether a list of elements are unique. 0 is ignored in the process."""

    c = Counter(line)
    del c[0]
    return set(c.values()) == {1}