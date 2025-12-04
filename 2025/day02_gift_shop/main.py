# AoC 2025 Day 2: https://adventofcode.com/2025/day/2
import argparse


def read_ranges(filename):
    with open(filename, 'r') as file:
        return file.read().split(',')


def split_string(word, n):
    return [word[i:i+n] for i in range(0, len(word), n)]


def id_is_invalid(product_id):
    length = len(product_id)
    for i in range(1, length):
        if len(set(split_string(product_id, i))) == 1:
            return True
    return False


def part1(id_ranges):
    invalid_sum = 0
    for id_range in id_ranges:
        left, right = id_range.split('-')
        for product_id in range(int(left), int(right)+1):
            product_str = str(product_id)
            length = len(product_str)
            if length % 2 != 0:
                continue
            mid = length >> 1
            if product_str[:mid] == product_str[mid:]:
                invalid_sum += product_id
    return invalid_sum


def part2(id_ranges):
    invalid_sum = 0
    for id_range in id_ranges:
        left, right = id_range.split('-')

        for product_id in range(int(left), int(right)+1):
            if id_is_invalid(str(product_id)):
                invalid_sum += product_id
    return invalid_sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    ranges = read_ranges(args.filename)

    print(f"Part1: {part1(ranges)}")
    print(f"Part2: {part2(ranges)}")
