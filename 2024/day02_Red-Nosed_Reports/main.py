import argparse


def is_safe(report):
    c = -1 if report[1] - report[0] < 0 else 1

    for prev, curr in zip(report, report[1:]):
        d = c * (curr - prev)
        if d < 1 or d > 3:
            return False
    return True


def solve(filename):
    safe_ct = 0
    dampened_safe_ct = 0
    with open(filename, 'r') as file:
        for report in file:
            parsed = list(map(int, report.split()))

            if is_safe(parsed):
                safe_ct += 1
            else:
                # Brute force... try removing 1 until we get safe
                for i in range(len(parsed)):
                    dampened_report = parsed[:i] + parsed[i + 1:]
                    if is_safe(dampened_report):
                        dampened_safe_ct += 1
                        break
    return (safe_ct, safe_ct + dampened_safe_ct)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    safe_ct, safe_ct_with_dampener = solve(args.filename)

    print(f"Part1: safe_ct = {safe_ct}")
    print(f"Part2: safe_ct_with_dampener = {safe_ct_with_dampener}")
