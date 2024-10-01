from typing import Optional
from pathlib import Path
from time import time
from argparse import ArgumentParser, Namespace
from sudoku import load_sudoku, Sudoku, assert_sudoku_valid, display


class Unsolvable(Exception):
    """The given problem has no solution."""


def parse_args(raw_args: Optional[list[str]]=None) -> Namespace:
    """Parse arguments from commandline."""

    arg_parser = ArgumentParser(description="Sudoku solver")
    arg_parser.add_argument("path", type=Path, help="Path from the input file")
    arg_parser.add_argument("-o", "--output", type=Path, help="File where to output the result.")
    return arg_parser.parse_args(raw_args)
        

def possible_values(cell: tuple[int, int], sudoku: Sudoku) -> set[int]:
    """Return all possible values for a cell (node consistency)."""

    x, y = cell
    # gather values from line
    values = set(sudoku[x])
    # gather values from columns
    values |= { sudoku[i][y] for i in range(9) }
    # gather values from chunks
    chunk = x // 3, y // 3  
    values |= { c for i in range(3) for c in sudoku[chunk[0] * 3 + i][chunk[1] * 3:(chunk[1] + 1) * 3]}
    # return possible values
    return set(range(1, 10)) - values


def solve(s: Sudoku):
    """Resolve sudoku."""

    missing_values = [(i, j) for i in range(9) for j in range(9) if s[i][j] == 0]
    possibles = [list[int]() for _ in missing_values]
    current = 0

    while current < len(missing_values):

        # update domain constraints
        possibles[current] = list(possible_values(missing_values[current], s))

        # backtracks
        while not possibles[current]:
            i, j = missing_values[current]
            s[i][j] = 0
            current -=1
            if current == -1:
                raise Unsolvable

        # explore
        i, j = missing_values[current]
        s[i][j] = possibles[current].pop()
        current += 1


if __name__ == "__main__":

    args = parse_args()
    sudoku = load_sudoku(args.path)
    display(sudoku)
    input("Press a key to solve the sudoku:")
    print("Solving...")

    try:
        t0 = time()
        solve(sudoku)
        elapsed = time() - t0
    except Unsolvable:
        print("xxx  The sudoku has no solutions  xxx")
        exit(1)
    else:
        assert_sudoku_valid(sudoku)
        print(f"\nGame solved in {elapsed:.5f}s:\n",)
        display(sudoku)

    if args.output is not None:
        with open(args.output, "w", encoding="utf-8") as f:
            display(sudoku, file=f)
