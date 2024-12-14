import argparse
import numpy as np


class ClawMachine:
    def __init__(self, a_btn, b_btn, prize):
        self.a = a_btn
        self.b = b_btn
        self.prize = prize

    def solve(self, unit_conversion_error=False):
        if unit_conversion_error:
            self.prize = (self.prize[0] + 10000000000000,
                          self.prize[1] + 10000000000000)

        # Set up system
        a = np.array([
            [self.a[0], self.b[0]],
            [self.a[1], self.b[1]]
        ])
        b = np.array([self.prize[0], self.prize[1]])

        det = round(np.linalg.det(a))

        # No solution
        if det == 0:
            return 0, 0, False

        # Cramer's rule
        det_a = self.prize[0] * self.b[1] - self.b[0] * self.prize[1]
        det_b = self.a[0] * self.prize[1] - self.prize[0] * self.a[1]

        # Not evenly divisible
        if det_a % det != 0 or det_b % det != 0:
            return 0, 0, False

        # Calculate result
        a = det_a / det
        b = det_b / det
        return round(a), round(b), True

    def __repr__(self):
        return f"A: {self.a}, B: {self.b}, Prize: {self.prize}"


def read_input(filename):
    machines = []
    with open(filename, 'r') as file:
        lines = file.read().strip().split("\n")

    for i in range(0, len(lines), 4):
        # Parse button A
        button_a_line = lines[i].split(": ")[1]
        ax, ay = button_a_line.split(", ")
        ax = int(ax[2:])
        ay = int(ay[2:])

        # Parse button B
        button_b_line = lines[i + 1].split(": ")[1]
        bx, by = button_b_line.split(", ")
        bx = int(bx[2:])
        by = int(by[2:])

        # Parse prize
        prize_line = lines[i + 2].split(": ")[1]
        px, py = prize_line.split(", ")
        px = int(px[2:])
        py = int(py[2:])

        machines.append(ClawMachine((ax, ay), (bx, by), (px, py)))

    return machines


def solve(machines):
    p1_total = 0
    p2_total = 0
    for m in machines:

        a, b, solved = m.solve()
        if solved:
            p1_total += a*3 + b

        # Enable the "unit conversion error" for part 2
        a, b, solved = m.solve(True)
        if solved:
            p2_total += a * 3 + b

    return p1_total, p2_total


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    machines = read_input(args.filename)

    p1, p2 = solve(machines)
    print(f"Part1: p1 = {p1}")
    print(f"Part2: p2 = {p2}")

