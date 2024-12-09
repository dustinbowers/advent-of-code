import argparse
from itertools import batched


def read_input(filename):
    with open(filename, 'r') as file:
        line = file.readline().strip()
        return list(map(int, line))


def get_memory(layout):
    memory = []
    is_file = True
    file_id = 0
    for s in layout:
        if is_file:
            memory.extend([int(file_id)] * s)
            file_id += 1
        else:
            memory.extend([None] * s)

        is_file = not is_file

    return memory


def part1(memory):
    left = 0
    right = len(memory) - 1

    # Walk inwards from each side while
    # swapping "not None" from the right with "None" on the left
    while left < right:
        while memory[left] is not None:
            left += 1
        while memory[right] is None:
            right -= 1
        while (left < right
               and memory[left] is None
               and memory[right] is not None):
            memory[left], memory[right] = memory[right], memory[left]
            left += 1
            right -= 1

    # Calculate checksum
    s = 0
    for i, m in enumerate(memory):
        if m is None:
            continue
        s += i * m
    return s


def part2(layout):
    data_blocks = []
    free_blocks = []
    file_id = 0
    for b in batched(layout, 2):
        data_size, *rest = b
        empty_size = rest[0] if len(rest) == 1 else 0

        data_blocks.append([file_id] * data_size)
        free_blocks.append([[], empty_size])
        file_id += 1

    candidate_id = len(data_blocks)
    while candidate_id > 1:
        candidate_id -= 1
        candidate_data = data_blocks[candidate_id]

        # find an empty block for this candidate
        for i in range(candidate_id):
            if free_blocks[i][1] >= len(candidate_data):
                free_blocks[i][0].extend(candidate_data)
                free_blocks[i][1] -= len(candidate_data)
                data_blocks[candidate_id] = [None] * len(candidate_data)
                break

    # Calculate checksum
    s = 0
    pos = 0
    for i in range(len(data_blocks)):
        for d in data_blocks[i]:
            s += (d or 0) * pos
            pos += 1
        for d in free_blocks[i][0]:
            s += d * pos
            pos += 1
        pos += free_blocks[i][1]

    return s


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    layout = read_input(args.filename)

    checksum = part1(get_memory(layout))
    print(f"\nPart1: checksum = {checksum}")

    checksum = part2(layout)
    print(f"Part2: checksum = {checksum}\n")
