# AoC 2025 Day 8 - Playground - https://adventofcode.com/2025/day/8
import argparse
import math
import union_find


def read_input(filename: str):
    with open(filename, 'r') as file:
        return [tuple([int(n) for n in line.strip().split(",")]) for line in file]


def distance(box1, box2):
    dx = abs(box1[0] - box2[0])
    dy = abs(box1[1] - box2[1])
    dz = abs(box1[2] - box2[2])

    # we could use math.dist but we can skip the sqrt step for this task
    return dx**2 + dy**2 + dz**2


def part1(boxes, count):
    num_boxes = len(boxes)
    distances = []
    for i in range(num_boxes):
        for j in range(i, num_boxes):
            if i == j:
                continue
            distances.append((i, j, distance(boxes[i], boxes[j])))

    uf = union_find.UnionFind(num_boxes)

    sorted_dists = sorted(distances, key=lambda x: x[2])
    for _ in range(count):
        a, b, dist = sorted_dists.pop(0)
        uf.unite(a, b)

    set_sizes = sorted(map(len, uf.get_disjoint_sets()))
    return math.prod(set_sizes[-3:])


def part2(boxes):
    num_boxes = len(boxes)
    distances = [
        (i, j, distance(boxes[i], boxes[j]))
        for i in range(num_boxes)
        for j in range(i + 1, num_boxes)
    ]

    uf = union_find.UnionFind(num_boxes)

    for a, b, dist in sorted(distances, key=lambda x: x[2]):
        uf.unite(a, b)

        # This is not very efficient.... but it'll do
        if len(uf.get_disjoint_sets()) == 1:
            box_a, box_b = boxes[a], boxes[b]
            return box_a[0] * box_b[0]
    return


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    input = read_input(args.filename)
    print(f"Part1: {part1(input, 1000)}")
    print(f"Part2: {part2(input)}")
