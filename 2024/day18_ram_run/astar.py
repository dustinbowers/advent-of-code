import heapq


class Node:
    def __init__(self, position, parent=None):
        self.position = position
        self.parent = parent
        self.g = 0  # Cost from start to current node
        self.h = 0  # Heuristic (estimated cost from current to goal)
        self.f = 0  # Total cost (g + h)

    def __lt__(self, other):
        return self.f < other.f


def astar(grid, start, goal):
    open_set = []
    closed_set = set()

    start_node = Node(start)
    goal_node = Node(goal)

    heapq.heappush(open_set, start_node)

    while open_set:
        current_node = heapq.heappop(open_set)

        if current_node.position == goal_node.position:
            path = []
            while current_node:
                path.append(current_node.position)
                current_node = current_node.parent
            return path[::-1]

        closed_set.add(current_node.position)

        for neighbor in get_neighbors(current_node.position, grid):
            if neighbor in closed_set:
                continue

            neighbor_node = Node(neighbor, current_node)
            neighbor_node.g = current_node.g + 1
            neighbor_node.h = heuristic(neighbor, goal_node.position)
            neighbor_node.f = neighbor_node.g + neighbor_node.h

            if neighbor_node not in open_set:
                heapq.heappush(open_set, neighbor_node)

    return None


def get_neighbors(position, grid):
    neighbors = []
    x, y = position
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nx, ny = x + dx, y + dy
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]) and grid[nx][ny] == '.':
            neighbors.append((nx, ny))
    return neighbors


def heuristic(position, goal):
    return abs(position[0] - goal[0]) + abs(position[1] - goal[1])
