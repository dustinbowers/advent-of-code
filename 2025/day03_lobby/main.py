# AoC 2025 Day 3 - Lobby - https://adventofcode.com/2025/day/3
import argparse


def read_banks(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]


def find_max_joltage(bank: str, num_batteries):
    output = ''
    left = 0
    right = len(bank) - num_batteries + 1
    for n in range(num_batteries):
        subset = [int(digit) for digit in bank[left:right]]
        max_bat = max(subset)
        max_ind = subset.index(max_bat)

        output += str(max_bat)

        left += max_ind + 1
        right += 1
    return int(output)


def part1(banks):
    return sum(find_max_joltage(bank, 2) for bank in banks)


def part2(banks):
    return sum(find_max_joltage(bank, 12) for bank in banks)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    banks = read_banks(args.filename)
    print(f"Part1: {part1(banks)}")
    print(f"Part2: {part2(banks)}")
