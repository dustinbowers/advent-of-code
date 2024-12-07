import argparse
import re
import bisect
from collections import defaultdict


def read_input(filename):
    row_items = defaultdict(list)
    col_items = defaultdict(list)
    num_rows = None
    num_cols = None
    items = defaultdict(list)

    with open(filename, 'r') as file:
        r = 0
        for line in file:

            matches = [m.start() for m in re.finditer(r"[\/|\\-]", line)]

            if len(matches):
                row_items[r] = matches
            for m in matches:
                items[(r, m)] = line[m]

            r += 1

        num_rows = r
        num_cols = len(line.strip())

        for row, cols in row_items.items():
            for col in cols:
                col_items[col].append(row)

        for c in col_items:
            col_items[c] = sorted(col_items[c])

    return row_items, col_items, items, num_rows, num_cols


def first_less_than(items, x):
    idx = bisect.bisect_left(items, x)
    if idx > 0:
        return items[idx - 1]
    return None


def first_greater_than(items, x):
    idx = bisect.bisect_right(items, x)
    if idx < len(items):
        return items[idx]
    return None


def part1(row_items, col_items, items, num_rows, num_cols, start_pos=(0, -1), dir='>'):
    segments = set()

    def propagate_beam(cur_pos, dir):
        r, c = cur_pos
        new_r, new_c = r, c
        match dir:
            case '^':
                new_r = first_less_than(col_items[c], r)
                if new_r is None:
                    segments.add((r, c, 0, c))
                    return
            case '>':
                new_c = first_greater_than(row_items[r], c)
                if new_c is None:
                    segments.add((r, c, r, num_cols-1))
                    return
            case 'v':
                new_r = first_greater_than(col_items[c], r)
                if new_r is None:
                    segments.add((r, c, num_rows-1, c))
                    return
            case '<':
                new_c = first_less_than(row_items[r], c)
                if new_c is None:
                    segments.add((r, c, r, 0))
                    return
        new_segment = (r, max(0, c), new_r, new_c)
        if new_segment in segments:
            return
        segments.add((r, c, new_r, new_c))

        match items[(new_r, new_c)]:
            case '/':
                if dir == '^':
                    dir = '>'
                elif dir == '>':
                    dir = '^'
                elif dir == 'v':
                    dir = '<'
                elif dir == '<':
                    dir = 'v'
                propagate_beam((new_r, new_c), dir)
            case '\\':
                if dir == '^':
                    dir = '<'
                elif dir == '>':
                    dir = 'v'
                elif dir == 'v':
                    dir = '>'
                elif dir == '<':
                    dir = '^'
                propagate_beam((new_r, new_c), dir)
            case '|':
                if dir == '>' or dir == '<':
                    propagate_beam((new_r, new_c), '^')
                    propagate_beam((new_r, new_c), 'v')
                else:
                    propagate_beam((new_r, new_c), dir)
            case '-':
                if dir == '^' or dir == 'v':
                    propagate_beam((new_r, new_c), '<')
                    propagate_beam((new_r, new_c), '>')
                else:
                    propagate_beam((new_r, new_c), dir)

    propagate_beam(start_pos, dir)

    return segments


def get_covered_points(segments):
    covered_points = set()
    for r1, c1, r2, c2 in segments:
        if r1 == r2:
            for c in range(min(c1, c2), max(c1, c2) + 1):
                covered_points.add((r1, c))
        elif c1 == c2:
            for r in range(min(r1, r2), max(r1, r2) + 1):
                covered_points.add((r, c1))
    return covered_points


def part2(row_items, col_items, items, num_rows, num_cols):
    energies = []

    def calculate_edge_energy(start_pos, dir):
        segments = part1(
            row_items, col_items, items, num_rows, num_cols, start_pos, dir)

        energized_points = get_covered_points(segments)
        return len(energized_points) - 1

    for c in range(num_cols+1):
        energies.append(calculate_edge_energy((-1, c), 'v'))
        energies.append(calculate_edge_energy((num_rows+1, c), '^'))

    for r in range(num_rows+1):
        energies.append(calculate_edge_energy((r, -1), '>'))
        energies.append(calculate_edge_energy((r, num_cols+1), '<'))

    return max(energies)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # Parse Input
    row_items, col_items, items, num_rows, num_cols = read_input(args.filename)

    # Part 1
    segments = part1(
        row_items, col_items, items, num_rows, num_cols)
    energized_points = get_covered_points(segments)
    energized_ct = len(energized_points) - 1

    # Part 2
    max_energized = part2(row_items, col_items, items, num_rows, num_cols)

    print(f"Part1: energized_ct = {energized_ct}")
    print(f"Part2: max_energized = {max_energized}")
