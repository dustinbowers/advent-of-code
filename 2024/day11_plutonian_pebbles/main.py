import argparse
import functools


def read_input(filename):
    with open(filename, 'r') as file:
        return list(map(int, file.readline().split(" ")))


def solve(stones, num_blinks):
    return sum([count_resulting_stones(s, num_blinks) for s in stones])


@functools.cache
def count_resulting_stones(val, num_blinks):
    # Base case
    if num_blinks <= 0:
        return 1

    # If val is 0 or odd number of digits, just modify and keep going
    s_str = str(val)
    if val == 0:
        return count_resulting_stones(1, num_blinks - 1)
    elif len(s_str) % 2 == 1:
        return count_resulting_stones(val * 2024, num_blinks - 1)

    # If val has an even number of digits we split the stone into two and keep going
    mid = int(len(s_str) / 2)
    left = int(s_str[:mid])
    right = int(s_str[mid:])
    return count_resulting_stones(left, num_blinks - 1) + count_resulting_stones(right, num_blinks - 1)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    stones = read_input(args.filename)

    p1 = solve(stones, 25)
    print(f"\nPart1: stones = {p1}")

    p2 = solve(stones, 75)
    print(f"\nPart2: stones = {p2}")
