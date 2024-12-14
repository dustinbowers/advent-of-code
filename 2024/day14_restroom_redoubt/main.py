import argparse
import math
from collections import defaultdict


WIDTH = 101
HEIGHT = 103
CENTER_LINE = math.floor(WIDTH / 2)
MID_LINE = math.floor(HEIGHT / 2)


class Robot:
    def __init__(self, px, py, vx, vy):
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy

    def __repr__(self):
        return f"Robot - pos: ({self.px}, {self.py}), velocity: ({self.vx}, {self.vy})"

    def step(self, seconds):
        self.px += self.vx * seconds
        self.px %= WIDTH

        self.py += self.vy * seconds
        self.py %= HEIGHT

    def get_quadrant(self):
        quad = None
        if self.px < CENTER_LINE and self.py < MID_LINE:
            quad = 0
        elif self.px > CENTER_LINE and self.py < MID_LINE:
            quad = 1
        elif self.px < CENTER_LINE and self.py > MID_LINE:
            quad = 2
        elif self.px > CENTER_LINE and self.py > MID_LINE:
            quad = 3
        return quad


def read_input(filename):
    robots = []
    with open(filename, 'r') as file:
        for line in file:
            p, v = line.split(" ")
            px, py = list(map(int, p[2:].split(",")))
            vx, vy = list(map(int, v[2:].split(",")))

            robots.append(Robot(px, py, vx, vy))

    return robots


def part1(robots, seconds):
    quad_ct = defaultdict(int)
    for r in robots:
        r.step(seconds)
        quad_ct[r.get_quadrant()] += 1

    res = 1
    for k in range(4):
        v = quad_ct[k]
        res *= v

    return res


def part2(robots):
    seconds = 0
    while True:
        for r in robots:
            r.step(1)
        seconds += 1

        positions = set((r.py, r.px) for r in robots)
        if len(positions) == len(robots):
            display_robots(robots)
            return seconds


def display_robots(robots):
    grid = list(['.'] * WIDTH for _ in range(HEIGHT+1))

    for r in robots:
        grid[r.py][r.px] = '#'

    for row in grid:
        print(f"r: {''.join(row)}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    if "example" in args.filename:
        WIDTH = 11
        HEIGHT = 7
        CENTER_LINE = math.floor(WIDTH / 2)
        MID_LINE = math.floor(HEIGHT / 2)

    robots = read_input(args.filename)

    p1 = part1(robots, 100)

    # Don't forget to add previous 100 steps in part 1 to P2
    p2 = part2(robots) + 100

    print(f"\nPart1: p1 = {p1}")
    print(f"\nPart2: p2 = {p2}")
