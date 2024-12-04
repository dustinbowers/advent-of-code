import re
import argparse
from collections import defaultdict


def get_diagonals_and_anti_diagonals(matrix):
    diagonals = defaultdict(list)
    anti_diagonals = defaultdict(list)
    for r, row in enumerate(matrix):
        for c, val in enumerate(row):
            diagonals[r - c].append(val)
            anti_diagonals[r + c].append(val)
    return list(diagonals.values()), list(anti_diagonals.values())


def read_input(filename):
    with open(filename, 'r') as file:
        input = [list(line.strip()) for line in file]

    rows = " ".join(["".join(r) for r in input])
    cols = " ".join(["".join(line) for line in [list(col)
                    for col in list(zip(*input))]])
    diag, anti_diag = get_diagonals_and_anti_diagonals(input)
    diag = " ".join(["".join(line) for line in diag])
    anti_diag = " ".join(["".join(line) for line in anti_diag])

    return input, rows, cols, diag, anti_diag


def part1(rows, cols, diag, anti_diag):
    total_input = " ".join([rows, cols, diag, anti_diag])
    xmas_count = len(re.findall("XMAS", total_input))
    xmas_count += len(re.findall("SAMX", total_input))
    return xmas_count


def part2(input):
    mas_count = 0
    for i in range(1, len(input)-1):
        for j in range(1, len(input[0])-1):
            if input[i][j] != 'A':
                continue
            diag = "".join([input[i-1][j-1], 'A', input[i+1][j+1]])
            anti_diag = "".join([input[i+1][j-1], 'A', input[i-1][j+1]])
            if (diag == 'MAS' or diag == 'SAM') and (anti_diag == 'MAS' or anti_diag == 'SAM'):
                mas_count += 1
    return mas_count


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    input, rows, cols, diag, anti_diag = read_input(args.filename)
    xmas_count = part1(rows, cols, diag, anti_diag)
    mas_count = part2(input)

    print(f"Part1: xmas_count = {xmas_count}")
    print(f"Part2: mas_count = {mas_count}")
