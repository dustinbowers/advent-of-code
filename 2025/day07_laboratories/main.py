# AoC 2025 Day 7- Laboratories - https://adventofcode.com/2025/day/7
import argparse


def read_input(filename: str):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def part1(grid):
    rows = len(grid)
    num_splits = 0

    # initialize beam propagation
    start_pos = grid[0].index('S')
    grid[1][start_pos] = '|'

    # propagate beams downward
    for i in range(rows-1):
        for ind, cell in enumerate(grid[i]):
            if cell != '|':
                continue
            if grid[i+1][ind] == '.':
                grid[i+1][ind] = '|'
            elif grid[i+1][ind] == '^':
                num_splits += 1
                if grid[i+1][ind-1] == '.':
                    grid[i+1][ind-1] = '|'
                if grid[i+1][ind+1] == '.':
                    grid[i+1][ind+1] = '|'

    return num_splits


def part2(grid):
    rows = len(grid)
    cols = len(grid[0])
    start_pos = grid[0].index("S")

    # initialize a grid counts
    counts = [[0 for i in range(cols)] for i in range(rows)]
    counts[0][start_pos] = 1

    # propagate counts downward
    for i in range(rows-1):
        for j in range(cols):
            if grid[i][j] != '|':
                continue

            counts[i][j] += counts[i-1][j]
            if grid[i+1][j] == '^':
                counts[i+1][j-1] += counts[i][j]
                counts[i+1][j+1] += counts[i][j]
    return sum(counts[rows-2])


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    input = read_input(args.filename)

    print(f"Part1: {part1(input)}")
    print(f"Part2: {part2(input)}")
