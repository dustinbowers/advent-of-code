import argparse


def read_input(filename):
    calibrations = []
    with open(filename, 'r') as file:
        for line in file:
            parts = line.split(":")
            total = int(parts[0])
            operands = list(map(int, (o for o in parts[1].split())))

            calibrations.append((total, operands))

    return calibrations


def solve(calibrations, concat_enabled):
    def backtrack(target, operands, current_index, current_value, concat_enabled):
        # Early out
        if current_value > target:
            return None

        # Base
        if current_index == len(operands):
            if current_value == target:
                return True
            return None

        next_operand = operands[current_index]

        result_add = backtrack(
            target,
            operands,
            current_index + 1,
            current_value + next_operand,
            concat_enabled)
        if result_add:
            return result_add

        result_multiply = backtrack(
            target,
            operands,
            current_index + 1,
            current_value * next_operand,
            concat_enabled)
        if result_multiply:
            return result_multiply

        if concat_enabled:
            result_concat = backtrack(
                target,
                operands,
                current_index + 1,
                int(f"{current_value}{next_operand}"),
                concat_enabled)
            if result_concat:
                return result_concat

        return None

    calibration_sum = 0
    for c in calibrations:
        target, operands = c

        if len(operands) == 1:
            if operands[0] == target:
                calibration_sum += target
            continue

        res = backtrack(target,
                        operands,
                        1,
                        operands[0],
                        concat_enabled)
        if res:
            calibration_sum += c[0]

    return calibration_sum


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # Parse Input
    calibrations = read_input(args.filename)

    # Solve
    p1 = solve(calibrations, concat_enabled=False)
    p2 = solve(calibrations, concat_enabled=True)

    print(f"\nPart1: {p1}")
    print(f"Part2: {p2}")
