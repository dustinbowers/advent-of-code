import argparse
import itertools


def read_input(filename):
    calibrations = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(":")
            total = int(parts[0])
            operands = list(map(int, (o for o in parts[1].split())))

            calibrations.append((total, operands))

    return calibrations


def solve(calibrations, operations):
    calibration_sum = 0
    for c in calibrations:
        target, nums = c
        ops = list(itertools.product(operations, repeat=len(nums)-1))

        for seq in ops:
            cur = nums[0]
            expression = str(cur)
            actions = list(zip(seq, nums[1:]))
            for action in actions:
                match action[0]:
                    case '*':
                        cur *= action[1]
                    case '+':
                        cur += action[1]
                    case '||':
                        cur = int(f"{cur}{action[1]}")
                expression = f"{expression} {action[0]} {action[1]}"
            if cur == target:
                print(f"found solution: {expression} = {cur}")
                calibration_sum += cur
                break

    return calibration_sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # Parse Input
    calibrations = read_input(args.filename)

    # Solve
    p1 = solve(calibrations, ["*", "+"])
    p2 = solve(calibrations, ["*", "+", "||"])

    print(f"\nPart1: {p1}")
    print(f"Part2: {p2}\n")
