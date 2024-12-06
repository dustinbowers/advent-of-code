import bisect
import argparse
from collections import defaultdict


def read_input(filename):
    start_pos = None
    row_obstacles = defaultdict(list)
    col_obstacles = defaultdict(list)
    num_rows = None
    num_cols = None
    with open(filename, 'r') as file:
        r = 0
        # Build a dictionary of row_ind => list of column indices
        for line in file:
            if start_pos is None:
                pos = line.find('^')
                if pos != -1:
                    start_pos = (r, pos)

            obs = [i for i, char in enumerate(line) if char == '#']
            if len(obs):
                row_obstacles[r] = obs
            r += 1

        num_rows = r
        num_cols = len(line)

        # Build a dictionary of col_ind => list of row indices
        for row, cols in row_obstacles.items():
            for col in cols:
                col_obstacles[col].append(row)

        # Sort the column row indices for later
        for c in col_obstacles:
            col_obstacles[c] = sorted(col_obstacles[c])

    return row_obstacles, col_obstacles, start_pos, num_rows, num_cols


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


def patrol(row_obstacles, col_obstacles, num_rows, num_cols, start_pos):
    """ Simulate a guard walking through a set of obstacles

    Returns:
        A list of line segment tuples indicating guard movement if no cycles are found,
        otherwise returns None to indicate a cycle has been encountered
    """
    dir = '^'
    r, c = start_pos
    segments = set()

    while True:
        new_c = c
        new_r = r
        match dir:
            case '^':  # Jump up to nearest obstacle
                obs_r = first_less_than(col_obstacles[c], r)
                if obs_r is None:  # break when out-of-bounds
                    segments.add((r, c, 0, c))
                    break
                new_r = obs_r + 1
                dir = '>'
            case '>':  # Jump right
                obs_c = first_greater_than(row_obstacles[r], c)
                if obs_c is None:
                    segments.add((r, c, r, num_cols-1))
                    break
                new_c = obs_c - 1
                dir = 'v'
            case 'v':  # Jump down
                obs_r = first_greater_than(col_obstacles[c], r)
                if obs_r is None:
                    segments.add((r, c, num_rows-1, c))
                    break
                new_r = obs_r - 1
                dir = '<'
            case '<':  # Jump left
                obs_c = first_less_than(row_obstacles[r], c)
                if obs_c is None:
                    segments.add((r, c, r, 0))
                    break
                new_c = obs_c + 1
                dir = '^'

        new_segment = (r, c, new_r, new_c)
        if new_segment in segments:
            return None

        segments.add(new_segment)
        r = new_r
        c = new_c

    return segments


def find_patrol_cycles(covered_points, row_obstacles, col_obstacles, num_rows, num_cols, start_pos):
    """ Determine the number of places that an obstacle can be placed to cause a cycle

    Returns:
        Number of possible cycles found
    """
    num_cycles = 0
    for r, c in covered_points:

        # Add a new obstacle to test
        bisect.insort(row_obstacles[r], c)
        bisect.insort(col_obstacles[c], r)

        if patrol(row_obstacles, col_obstacles, num_rows, num_cols, start_pos) is None:
            num_cycles += 1

        # Remove previous obstacle
        row_obstacles[r].remove(c)
        col_obstacles[c].remove(r)

    return num_cycles


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


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # Load input
    row_obstacles, col_obstacles, start_pos, num_rows, num_cols = read_input(
        args.filename)

    # Part 1

    segments = patrol(row_obstacles, col_obstacles,
                      num_rows, num_cols, start_pos)

    covered_points = get_covered_points(segments)
    num_covered_points = len(covered_points)

    # Part 2

    # discard starting point when searching for cycles
    covered_points.discard((start_pos[0], start_pos[1]))

    num_cycles = find_patrol_cycles(
        covered_points, row_obstacles, col_obstacles, num_rows, num_cols, start_pos)

    print(f"\nPart1: steps_covered = {num_covered_points}")
    print(f"Part2: num_cycles = {num_cycles}\n")
