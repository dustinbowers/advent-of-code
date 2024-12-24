import argparse
import numpy as np


def read_input(filename):
    return [int(line.strip()) for line in open(filename)]


def calculate_next(num):

    total = num

    # multiply by 64, mix, prune
    r1 = total * 64
    total ^= r1
    total %= 16777216

    # divide by 32, mix, prune
    r2 = total // 32
    total ^= r2
    total %= 16777216

    # multiply by 2048, mix, prune
    r3 = total * 2048
    total ^= r3
    total %= 16777216

    return total


def part1(secrets):
    total = 0
    monkeys = []
    for s in secrets:
        n = s
        ones = [0] * 2001
        ones[0] = s % 10
        for i in range(1, 2001):
            n = calculate_next(n)
            ones[i] = n % 10
        monkeys.append(ones)
        total += n
    return total, monkeys


def part2(monkeys):
    seen_seq = {}
    for seq in monkeys:
        diffs = np.diff(seq)
        seen = set()
        for p in range(4, len(diffs)):
            h = tuple(diffs[p-3:p+1])
            if h not in seen_seq and h not in seen:
                seen_seq[h] = seq[p + 1]
            elif h not in seen:
                seen_seq[h] += seq[p + 1]
            seen.add(h)
    return max(seen_seq.values())


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    secrets = read_input(args.filename)

    p1_sum, monkeys = part1(secrets)
    print(f"Part1: p1_sum={p1_sum}")

    max_bananas = part2(monkeys)
    print(f"Part2: max_bananas={max_bananas}")
