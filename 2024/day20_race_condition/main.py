import argparse


def read_input(filename):
    grid = []
    start = None
    with open(filename, 'r') as file:
        r = 0
        for line in file:
            if start is None:
                ind = line.find('S')
                if ind != -1:
                    start = (r, ind)
            grid.append(list(line.strip()))
            r += 1
        return grid, start


def calculate_cost_grid(grid, start):
    cost_grid = list([float('-inf')] * len(grid[0]) for _ in range(len(grid)))

    r, c = start
    cost_grid[r][c] = 0
    cost = 1
    while grid[r][c] != 'E':
        for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
            nr, nc = r + dr, c + dc
            if grid[nr][nc] != "#" and cost_grid[nr][nc] == float('-inf'):
                cost_grid[nr][nc] = cost
                cost += 1
                r, c = nr, nc
                break
    return cost_grid, cost-1


def part1(grid, start):
    cost_grid, max_cost = calculate_cost_grid(grid, start)

    # Find cheats that save more than 100 picoseconds
    rows, cols = len(grid), len(grid[0])
    cheats = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                continue
            for dr, dc in [(-1, 1), (0, 2), (1, 1), (2, 0)]:
                nr, nc = r + dr, c + dc
                if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                    continue
                if grid[nr][nc] == '#':
                    continue
                if abs(cost_grid[r][c] - cost_grid[nr][nc]) >= 102:
                    cheats += 1

    return cheats


def part2(grid, start):
    cost_grid, max_cost = calculate_cost_grid(grid, start)

    # Find cheats that save more than 100 picoseconds
    rows, cols = len(grid), len(grid[0])
    cheats = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == '#':
                continue
            for radius in range(2, 21):
                for dr in range(radius + 1):
                    dc = radius - dr
                    for nr, nc in {(r + dr, c + dc), (r - dr, c + dc), (r + dr, c - dc), (r - dr, c - dc)}:
                        if nr < 0 or nc < 0 or nr >= rows or nc >= cols:
                            continue
                        if grid[nr][nc] == '#':
                            continue
                        if cost_grid[r][c] - cost_grid[nr][nc] >= 100 + radius:
                            cheats += 1
    return cheats


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    grid, start = read_input(args.filename)

    cheats_2 = part1(grid, start)
    print(f"\nPart1: cheats_2 = {cheats_2}")
    cheats_20 = part2(grid, start)
    print(f"Part2: cheats_20 = {cheats_20}\n")
