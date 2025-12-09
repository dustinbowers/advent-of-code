# AoC 2025 Day 9 - Movie Theater - https://adventofcode.com/2025/day/9
import argparse
import itertools


def read_input(filename: str):
    with open(filename, 'r') as file:
        return [[int(n) for n in line.strip().split(",")] for line in file]


def part1(points):
    pairs = list(itertools.combinations(points, 2))
    max_area = 0
    for pair in pairs:
        a, b = pair[0], pair[1]
        area = (abs(a[0] - b[0])+1) * (abs(a[1] - b[1])+1)
        if area > max_area:
            max_area = area
    return max_area


def part2(points):
    pairs = list(itertools.combinations(points, 2))
    max_area = 0
    for pair in pairs:
        a, b = tuple(pair[0]), tuple(pair[1])

        # skip backwards pairs
        if a > b:
            continue

        # pre-calculate edges
        left_edge = min(a[0], b[0])
        right_edge = max(a[0], b[0])
        top_edge = min(a[1], b[1])
        bottom_edge = max(a[1], b[1])

        # look for intersecting lines
        for i in range(len(points)):
            point_one = points[i]
            point_two = points[(i+1) % len(points)]

            # skip backwards points
            if tuple(point_one) > tuple(point_two):
                continue

            # break if intersecting line is found
            if not (
                    max(point_one[0], point_two[0]) <= left_edge or
                    right_edge <= min(point_one[0], point_two[0]) or
                    max(point_one[1], point_two[1]) <= top_edge or
                    bottom_edge <= min(point_one[1], point_two[1])):
                break
        else:
            # save largest area of unobstructed box
            area = (abs(a[0] - b[0])+1) * (abs(a[1] - b[1])+1)
            max_area = max(max_area, area)
    return max_area


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    points = read_input(args.filename)
    print(f"Part1: {part1(points)}")
    print(f"Part2: {part2(points)}")
