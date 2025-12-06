# AoC 2025 Day 6 - Trash Compactor - https://adventofcode.com/2025/day/6
import math
import argparse


def read_input(filename: str):
    with open(filename, 'r') as file:
        return file.read()


def part1(input):
    nums = []
    operators = []
    input = input.strip().split("\n")
    operators = input.pop().split()
    nums = [line.split() for line in input]

    # convert and transpose nums
    int_nums = []
    for i in range(len(nums)):
        int_nums.append([int(num) for num in nums[i]])
    int_nums = [list(row) for row in zip(*int_nums)]

    total = 0
    for i, op in enumerate(operators):
        if op == '*':
            total += math.prod(int_nums[i])
        else:
            total += sum(int_nums[i])
    return total


def part2(input):
    # split into a list of lists of characters
    grid = [list(line) for line in input.split("\n")[:-1]]

    # transpose
    grid = [list(row) for row in zip(*grid)]

    # append a terminating row
    empty_row = [' '] * len(grid[0])
    grid.append(empty_row)

    total = 0
    curr_list = []
    op = ''
    for row in grid:
        # catch the current operator when we find one
        if row[-1] != ' ':
            op = row[-1]

        # empty row triggers a conclusion to current section
        if row == empty_row:
            if op == '*':
                total += math.prod(curr_list)
            else:
                total += sum(curr_list)
            curr_list = []
            continue

        # add current section's number to a list for later maths
        curr_list.append(int("".join(row[:-1])))

    return total


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    file_contents = read_input(args.filename)
    print(f"Part1: {part1(file_contents)}")
    print(f"Part2: {part2(file_contents)}")
