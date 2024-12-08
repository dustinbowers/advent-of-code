import argparse
import re
from collections import defaultdict


def read_input(filename):
    """ Reads input and returns the antenna labels and their positions

        Returns:
            A dictionary of antenna labels that map to a list of 
            tuple positions for each antenna
    """
    antennas = defaultdict(list)
    with open(filename, 'r') as file:
        r = 0
        for line in file:
            ants = [(line[m.start()], m.start())
                    for m in re.finditer("[^.]", line.strip())]
            for a in ants:
                antennas[a[0]].append((r, a[1]))
            r += 1
    return antennas, r, len(line.strip())


def find_anti_node(r1, c1, r2, c2, multiple=1):
    return (r2 + (multiple * (r2 - r1)), c2 + (multiple * (c2 - c1)))


def part1(antennas, num_rows, num_cols):
    anti_nodes = set()
    for a, pts in antennas.items():
        for (r1, c1) in pts:
            for (r2, c2) in pts:
                if (r1, c1) == (r2, c2):
                    continue
                anti_node = find_anti_node(r1, c1, r2, c2)
                if (anti_node[0] < 0 or anti_node[0] >= num_rows or anti_node[1] < 0 or anti_node[1] >= num_cols):
                    continue
                anti_nodes.add(anti_node)
    return anti_nodes


def part2(antennas, num_rows, num_cols):
    anti_nodes = set()
    for a, pts in antennas.items():
        for (r1, c1) in pts:
            anti_nodes.add((r1, c1))
    for a, pts in antennas.items():
        for (r1, c1) in pts:
            for (r2, c2) in pts:
                if (r1, c1) == (r1, c2):
                    continue
                dr, dc, multiple = 0, 0, 1
                while True:
                    dr, dc = find_anti_node(r1, c1, r2, c2, multiple)
                    if dr < 0 or dr >= num_rows or dc < 0 or dc >= num_cols:
                        break
                    anti_nodes.add((dr, dc))
                    multiple += 1
    return anti_nodes


def print_map(antennas, anti_nodes, num_rows, num_cols):
    grid = list(['.'] * num_cols for r in range(num_rows))
    for a in anti_nodes:
        grid[a[0]][a[1]] = '#'
    for a, pts in antennas.items():
        for (r1, c1) in pts:
            grid[r1][c1] = a
    for r in grid:
        print("".join(r))


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    # Parse Input
    antennas, num_rows, num_cols = read_input(args.filename)

    # Part 1
    anti_nodes = part1(antennas, num_rows, num_cols)

    # Part 2
    harmonic_anti_nodes = part2(antennas, num_rows, num_cols)

    # Print part 2 grid
    print_map(antennas, harmonic_anti_nodes, num_rows, num_cols)

    print(f"\nPart1: num_anti_nodes = {len(anti_nodes)}")
    print(f"Part2: num_harmonic_anti_nodes = {len(harmonic_anti_nodes)}\n")
