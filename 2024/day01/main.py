import argparse


def read_input(filename):
    with open(filename, 'r') as input:
        left, right = zip(*(map(int, line.split()) for line in input))
    return list(left), list(right)


def part1(left, right):
    return sum(abs(r-l) for l, r in zip(sorted(left), sorted(right)))


def part2(left, right):
    right_ct = {r: right.count(r) for r in set(right)}
    return sum(l * right_ct.get(l, 0) for l in left)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    left, right = read_input(args.filename)

    sort_dist = part1(left, right)
    print(f"Part 1: sort_dist = {sort_dist}")

    similarity_score = part2(left, right)
    print(f"Part2: similarity_score = {similarity_score}")
