# AoC 2025 Day 5 - Cafeteria - https://adventofcode.com/2025/day/5
import argparse


def read_input(filename: str):
    ranges = []
    ingredients = []
    with open(filename, 'r') as file:
        for line in file:
            if line == '\n':
                break
            start, end = line.strip().split("-")
            ranges.append((int(start), int(end)))
        for line in file:
            ingredients.append(int(line.strip()))
    return ranges, ingredients


def remove_overlaps(ranges: list[(int, int)]) -> list[(int, int)]:
    num_ranges = len(ranges)
    for i in range(num_ranges):
        i_s, i_e = ranges[i]
        for j in range(num_ranges):
            # Skip self-comparison and any ranges marked for removal
            if i == j or ranges[j] == (-1, -1):
                continue
            j_s, j_e = ranges[j]

            # if range J is entirely encapsulated by range I, mark range J for removal
            if j_s >= i_s and j_e <= i_e:
                ranges[j] = (-1, -1)
                continue

            # if range J extends OUT of range I, push range J's start forward
            if i_s <= j_s <= i_e:
                ranges[j] = (i_e + 1, j_e)
                continue

            # if range J extends INTO range I, pull range J's end backward
            if i_s <= j_e <= i_e:
                ranges[j] = (j_s, i_s - 1)
                continue

    # ensure ranges are unique, and remove invalid range
    merge_set = set(ranges)
    merge_set.remove((-1, -1))
    return list(merge_set)


def part1(ranges, ingredients):
    num_fresh = 0
    for ingredient in ingredients:
        spoiled = True
        for start, end in ranges:
            if start <= ingredient <= end:
                spoiled = False
                break
        if not spoiled:
            num_fresh += 1
    return num_fresh


def part2(ranges):
    return sum([e - s + 1 for s, e in remove_overlaps(ranges)])


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    ranges, ingredients = read_input(args.filename)
    print(f"Part1: {part1(ranges, ingredients)}")
    print(f"Part2: {part2(ranges)}")
