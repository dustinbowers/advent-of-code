import argparse


def read_input(filename):
    with open(filename, 'r') as file:
        return [list(line.strip()) for line in file]


def is_valid_pos(r, c, num_rows, num_cols):
    return (0 <= r < num_rows) and (0 <= c < num_cols)


def calculate_fence_price(grid):
    rows = len(grid)
    cols = len(grid[0])
    fences = 0
    area = 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != '.':  # Consider any non-empty space
                area += 1
                fences += 4  # start with 4 fence pieces

                # Check above
                if r > 0 and grid[r - 1][c] != '.':
                    fences -= 2  # shared edge with the cell above removes 2 fences

                # Check left
                if c > 0 and grid[r][c - 1] != '.':
                    fences -= 2  # shared edge with the cell to the left removes 2 fences

    return fences * area


def calculate_bulk_fence_price(grid):
    rows = len(grid)
    cols = len(grid[0])
    area = 0

    # Add a 1-thick padding around the region
    for r in range(rows):
        grid[r] = ['.', *grid[r], '.']
    pad_row = ['.'] * (cols + 2)

    grid.insert(0, pad_row)
    grid.append(pad_row)

    # Cound row-sides
    rows += 2
    cols += 2
    total_sides = 0
    for r in range(1, rows):
        edge_ct = 0
        dir = 0
        for c in range(cols):
            if grid[r][c] != '.':
                area += 1

            next_dir = 0
            if grid[r][c] != '.' and grid[r-1][c] == '.':
                next_dir = 1
            if grid[r][c] == '.' and grid[r-1][c] != '.':
                next_dir = -1

            if dir == next_dir:
                continue

            if next_dir != 0:
                edge_ct += 1
            dir = next_dir

        total_sides += edge_ct

    # Count col-sides
    for c in range(1, cols):
        edge_ct = 0
        dir = 0
        for r in range(rows):
            next_dir = 0
            if grid[r][c] != '.' and grid[r][c-1] == '.':
                next_dir = 1
            if grid[r][c] == '.' and grid[r][c-1] != '.':
                next_dir = -1

            if dir == next_dir:
                continue

            if next_dir != 0:
                edge_ct += 1
            dir = next_dir

        total_sides += edge_ct

    return total_sides * area


def solve(grid):
    num_rows, num_cols = len(grid), len(grid[0])
    visited = [[False] * num_cols for _ in range(num_rows)]

    # Use BFS to fill regions
    def walk_region(r, c):
        new_grid = [['.'] * num_cols for _ in range(num_rows)]
        queue = []
        queue.append((r, c))
        region_label = grid[r][c]
        new_grid[r][c] = region_label
        row_ids = set([r])
        col_ids = set([c])
        while queue:
            cur_r, cur_c = queue.pop(0)
            for dr, dc in [(-1, 0), (0, 1), (1, 0), (0, -1)]:
                nr, nc = cur_r + dr, cur_c + dc
                if not is_valid_pos(nr, nc, num_rows, num_cols):
                    continue
                if visited[nr][nc]:
                    continue
                if grid[nr][nc] == region_label:
                    queue.append((nr, nc))
                    visited[nr][nc] = True
                    new_grid[nr][nc] = region_label
                    row_ids.add(nr)
                    col_ids.add(nc)

        # Crop grid to save memory
        min_r, max_r = min(row_ids), max(row_ids)
        min_c, max_c = min(col_ids), max(col_ids)
        cropped_grid = []
        for r in range(min_r, max_r+1):
            cropped_grid.append(new_grid[r][min_c:max_c+1])

        # print("=== Region ===")
        # for r in cropped_grid:
        #     print(f"\t{''.join(r)}")

        # Calculate fence prices
        fence_price = calculate_fence_price(cropped_grid)
        bulk_fence_price = calculate_bulk_fence_price(cropped_grid)

        return fence_price, bulk_fence_price

    regular_price = 0
    bulk_price = 0

    # Walk the board looking for cells we haven't visited yet
    for r in range(num_rows):
        for c in range(num_cols):
            if visited[r][c]:
                continue
            fence_price, bulk_fence_price = walk_region(r, c)
            regular_price += fence_price
            bulk_price += bulk_fence_price

    return regular_price, bulk_price


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    grid = read_input(args.filename)

    p1, p2 = solve(grid)
    print(f"\nPart1: p1 = {p1}")
    print(f"Part2: p2 = {p2}\n")
