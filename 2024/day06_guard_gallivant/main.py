import copy
import argparse


def read_input(filename):
    raw_input = []
    start_pos = (0, 0)
    with open(filename, 'r') as file:
        for line in file:
            pos = line.find('^')
            if pos != -1:
                start_pos = (len(raw_input), pos)
            raw_input.append(line)

    room = [list(line.strip()) for line in raw_input]
    return room, start_pos


direction = {
    '^': (-1, 0),
    '>': (0,  1),
    'v': (1,  0),
    '<': (0, -1)
}


def turn_right(dir):
    match dir:
        case '^': return '>'
        case '>': return 'v'
        case 'v': return '<'
        case '<': return '^'


def next_step(cur_pos, dir):
    return (cur_pos[0] + direction[dir][0], cur_pos[1] + direction[dir][1])


def patrol(room, start_pos, obstacle=None):
    h = len(room)-1
    w = len(room[0])-1
    dir = '^'
    cur_pos = start_pos
    room[start_pos[0]][start_pos[1]] = 'X'
    dir_change = []
    if obstacle is not None:
        room[obstacle[0]][obstacle[1]] = 'O'
    while True:
        room[cur_pos[0]][cur_pos[1]] = 'X'
        next_pos = next_step(cur_pos, dir)
        if next_pos[0] < 0 or next_pos[0] > w or next_pos[1] < 0 or next_pos[1] > h:
            break
        if (room[next_pos[0]][next_pos[1]] == '#' or room[next_pos[0]][next_pos[1]] == 'O'):
            bump = (cur_pos[0], cur_pos[1], dir)
            if bump in dir_change:
                return -1  # found a cycle
            dir_change.append(bump)
            dir = turn_right(dir)
        else:
            cur_pos = next_pos

    return sum([line.count('X') for line in room]), room


def find_patrol_cycles(room, start_pos):
    h = len(room) - 1
    w = len(room[0]) - 1

    _, patrolled_room = patrol(room, start_pos)

    obstacles_that_cause_cycle = []
    for r in range(h):
        for c in range(w):
            if patrolled_room[r][c] != 'X':
                continue
            s = patrol(copy.deepcopy(room), start_pos, (r, c))
            if s == -1:
                obstacles_that_cause_cycle.append((r, c))

    return len(obstacles_that_cause_cycle)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    room, start_pos = read_input(args.filename)

    steps_covered, _ = patrol(room, start_pos)
    num_cycle_obstacles = find_patrol_cycles(room, start_pos)

    print(f"\nPart1: steps_covered = {steps_covered}")
    print(f"Part2: num_cycle_obstacles = {num_cycle_obstacles}\n")
