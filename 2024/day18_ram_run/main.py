import argparse
from astar import *

WIDTH = 70
HEIGHT = 70
P1_STEPS = 1024


def read_input(filename):
    blocks = []
    with open(filename, 'r') as file:
        for line in file:
            b = line.strip().split(",")
            blocks.append((int(b[1]), int(b[0])))
    return blocks


def part1(grid, blocks, num_corrupted):
    # Drop some blocks
    for n in range(num_corrupted):
        r, c = blocks[n]
        grid[r][c] = '#'

    path = astar(grid, (0, 0), (WIDTH, HEIGHT))

    return len(path)-1


def part2(grid, blocks):
    # Block the board with all pieces
    for (br, bc) in blocks:
        grid[br][bc] = '#'

    # Remove pieces until we unlock a valid path
    for (br, bc) in reversed(blocks):
        grid[br][bc] = '.'

        path = astar(grid, (0, 0), (WIDTH, HEIGHT))
        if path:
            return (br, bc)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()
    if "example" in args.filename:
        WIDTH = 6
        HEIGHT = 6
        P1_STEPS = 12

    grid = list(['.'] * (WIDTH + 1) for _ in range(HEIGHT + 1))
    blocks = read_input(args.filename)

    steps = part1(grid, blocks, P1_STEPS)
    key_block = part2(grid, blocks)

    print(f"\nPart 1: num_steps = {steps}")
    print(f"Part 2: key_block = {key_block[1]},{key_block[0]}")
