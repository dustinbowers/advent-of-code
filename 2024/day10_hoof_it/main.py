import argparse


def read_input(filename):
    grid = []
    trail_heads = []
    r = 0
    with open(filename, 'r') as file:
        for line in file:
            row = list(map(int, list(line.strip())))
            grid.append(row)
            for idx in range(len(row)):
                if row[idx] == 0:
                    # trail_heads.append(TrailHead(r, idx))
                    trail_heads.append((r, idx))
            r += 1
    return grid, trail_heads


def is_valid_pos(grid, r, c, num_rows, num_cols, current_height):
    if 0 <= r < num_rows and 0 <= c < num_cols:
        return grid[r][c] == current_height + 1
    return False


def part1(grid, trail_heads):
    num_rows, num_cols = len(grid), len(grid[0])

    def dfs(r, c, visited):
        stack = [(r, c)]
        reachable_nines = set()
        while stack:
            cur_r, cur_c = stack.pop()
            cur_height = grid[cur_r][cur_c]

            if cur_height == 9:
                reachable_nines.add((cur_r, cur_c))

            for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = cur_r + dr, cur_c + dc
                if is_valid_pos(grid, nr, nc, num_rows, num_cols, cur_height) and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    stack.append((nr, nc))
        return len(reachable_nines)

    total_score = 0
    for head in trail_heads:
        head_r, head_c = head
        visited = set((head_r, head_c))
        score = dfs(head_r, head_c, visited)
        total_score += score

    return total_score


def part2(grid, trail_heads):
    num_rows, num_cols = len(grid), len(grid[0])

    def dfs(r, c):
        stack = [(r, c)]
        score = 0
        while stack:
            cur_r, cur_c = stack.pop()
            cur_height = grid[cur_r][cur_c]

            if cur_height == 9:
                score += 1

            for (dr, dc) in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = cur_r + dr, cur_c + dc
                if is_valid_pos(grid, nr, nc, num_rows, num_cols, cur_height):
                    stack.append((nr, nc))
        return score

    total_score = 0
    for head in trail_heads:
        head_r, head_c = head
        score = dfs(head_r, head_c)
        total_score += score
    return total_score


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    grid, trail_heads = read_input(args.filename)

    p1 = part1(grid, trail_heads)
    print(f"\nPart1: total_score = {p1}")

    p2 = part2(grid, trail_heads)
    print(f"Part2: total_score = {p2}\n")
