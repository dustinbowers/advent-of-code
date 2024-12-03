import argparse
import re


def solve(filename):
    with open(filename, 'r') as file:
        total_input = ''.join(line.rstrip() for line in file)

    p1 = sum(int(a) * int(b)
             for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", total_input))

    cleaned_input = re.sub(r"don't\(\).*?do\(\)", "", total_input)
    cleaned_input = re.sub(r"don't\(\).*", "", cleaned_input)

    p2 = sum(int(a) * int(b)
             for a, b in re.findall(r"mul\((\d{1,3}),(\d{1,3})\)", cleaned_input))

    return p1, p2


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # p1 = part1(args.filename)
    # p2 = part2(args.filename)
    p1, p2 = solve(args.filename)

    print(f"Part1: sum = {p1}")
    print(f"Part2: sum = {p2}")
