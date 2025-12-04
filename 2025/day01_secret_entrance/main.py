# AoC 2025 Day 1: https://adventofcode.com/2025/day/1
import argparse


def line_to_move(line):
    return (line[0], int(line[1:]))


def read_input(filename):
    with open(filename, 'r') as file:
        return [line_to_move(line.strip()) for line in file]


def solve(moves):
    zero_hits = 0
    zero_crosses = 0

    dial_positions = 100
    target = 0
    current = 50
    for move in moves:
        dir = move[0]
        dist = move[1]

        full_rotations = dist // 100
        zero_crosses += full_rotations

        rem = dist % 100
        if current != 0 and \
            (dir == 'L' and current - rem < 0) or \
                (dir == 'R' and current + rem > 100):
            zero_crosses += 1

        current += rem * (-1 if dir == 'L' else 1)
        current %= dial_positions
        if current == target:
            zero_hits += 1
    return zero_hits, zero_crosses


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    moves = read_input(args.filename)
    zero_hit_count, zero_crosses = solve(moves)

    print(f"Part1: {zero_hit_count}")
    print(f"Part2: {zero_hit_count + zero_crosses}")
