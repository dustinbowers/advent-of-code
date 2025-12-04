# AoC 2025 Day 4 - Lobby - https://adventofcode.com/2025/day/4
import argparse


def read_field(filename: str) -> list[list[str]]:
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def get_position(field, rows, cols, i, j) -> bool:
    if i < 0 or j < 0 or i >= rows or j >= cols:
        return '.'
    return field[i][j]


def part1(field):
    moveable = 0
    rows = len(field)
    cols = len(field[0])

    new_field = []

    for i, row in enumerate(field):
        new_row = []
        for j, cell in enumerate(row):
            if cell == '.':
                new_row.append('.')
                continue
            adj = 0
            for y in range(-1, 2):
                for x in range(-1, 2):
                    if x == 0 and y == 0:
                        continue
                    check_cell = get_position(field, rows, cols, i+y, j+x)
                    if check_cell == '@':
                        adj += 1
            if adj < 4:
                new_row.append('.')
                moveable += 1
            else:
                new_row.append('@')
        new_field.append(new_row)
    return moveable, new_field


def part2(field):

    total_moved = 0
    while True:
        num_moveable, field = part1(field)
        total_moved += num_moveable
        if num_moveable == 0:
            break

    return total_moved


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    field = read_field(args.filename)

    print(f"Part1: {part1(field)[0]}")
    print(f"Part2: {part2(field)}")
