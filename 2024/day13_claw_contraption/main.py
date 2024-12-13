import argparse
import re


class ClawMachine:
    def __init__(self, a_btn, b_btn, prize):
        self.a = a_btn
        self.b = b_btn
        self.prize = prize

    def solve(self, unit_conversion_error=False):
        if unit_conversion_error:
            self.prize = (self.prize[0]+10000000000000,
                          self.prize[1] + 10000000000000)

        a_m = self.a[1] / self.a[0]  # Slope A
        b_m = self.b[1] / self.b[0]  # Slope B
        b_intercept = self.prize[1] - (b_m * self.prize[0])
        c_m = a_m - b_m

        # Calculate number of "A" presses
        intersection_x = b_intercept / c_m
        a = round(intersection_x / self.a[0])

        # Calculate number of "B" presses
        intersection_y = intersection_x * a_m
        b = round((self.prize[1] - intersection_y) / self.b[1])

        if (a * self.a[0] + b * self.b[0] != self.prize[0]) \
                or (a * self.a[1] + b * self.b[1] != self.prize[1]):
            return 0, 0, False
        return a, b, True

    def __repr__(self):
        return f"A: {self.a}, B: {self.b}, Prize: {self.prize}"


def read_input(filename):
    machines = []
    with open(filename, 'r') as file:
        while True:
            a_xy = re.findall(r"^Button A: X\+(\d+?), Y\+(\d+?)$",
                              file.readline().strip())
            b_xy = re.findall(r"^Button B: X\+(\d+?), Y\+(\d+?)$",
                              file.readline().strip())
            prize = re.findall(r"^Prize: X=(\d+?), Y=(\d+?)$",
                               file.readline().strip())

            machines.append(ClawMachine(
                tuple(map(int, a_xy[0])),
                tuple(map(int, b_xy[0])),
                tuple(map(int, prize[0]))))

            if not file.readline():
                break

    return machines


def solve(machines):

    p1_total = 0
    p2_total = 0
    for m in machines:

        a, b, solved = m.solve()
        if solved:
            p1_total += a*3 + b

        # Enable the "unit conversion error"
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
