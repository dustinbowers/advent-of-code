import argparse


def read_input(filename):
    with open(filename, 'r') as file:
        groups = file.read().split("\n\n")
        elves = [list(map(int, g.strip().split("\n"))) for g in groups]
    return elves


def part1(elves):
    return max([sum(e) for e in elves])


def part2(elves):
    s = [sum(e) for e in elves]
    return sum(sorted(s)[-3:])


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()
    elves = read_input(args.filename)

    p1 = part1(elves)
    print(f"Part1: max_calories = {p1}")

    p2 = part2(elves)
    print(f"Part2: sum_3_calories = {p2}")
