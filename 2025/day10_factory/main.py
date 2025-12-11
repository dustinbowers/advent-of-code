# AoC 2025 Day 10 - Factory - https://adventofcode.com/2025/day/10
import argparse
import z3
from collections import deque


def read_input(filename: str):
    machines = []
    with open(filename, 'r') as file:
        # Wheww, messy messy
        for line in file:
            line = line.strip()
            bracket_pos = line.find(" ")
            curly_pos = line.rfind(" ")
            light_indicators = [c == '#' for c in line[1:bracket_pos-1]]
            wiring_schematic = [list(map(int, split[1:-1].split(",")))
                                for split in line[bracket_pos+1:curly_pos].split(" ")]
            joltage = [int(joltage)
                       for joltage in line[curly_pos+2:-1].split(",")]
            machines.append([light_indicators, wiring_schematic, joltage])

    return machines


def toggle_buttons(current_state, buttons):
    new_state = current_state.copy()
    for ind in buttons:
        new_state[ind] ^= True
    return new_state


def part1(machines):
    answer_presses = []
    for machine in machines:
        target = machine[0]
        wiring = machine[1]

        queue = deque()
        queue.append([[False] * len(target), []])
        while queue:
            current_node, button_presses = queue.popleft()

            # explore "neighbors"
            for i, buttons in enumerate(wiring):
                result = toggle_buttons(current_node, buttons)
                queue.append([result, button_presses + [i]])
                if result == target:
                    queue.clear()
                    answer_presses.append(len(button_presses) + 1)
                    break

    return sum(answer_presses)


def part2(machines):
    answer_presses = []
    for machine in machines:
        # model the problem
        joltages = machine[2]
        wiring = machine[1]
        presses = [z3.Int(f"wire_set_{i}") for i in range(len(wiring))]
        s = z3.Optimize()

        # add constraints
        s.add(z3.And([press >= 0 for press in presses]))
        constraints = [
            sum(presses[j] for j, button in enumerate(
                wiring) if i in button) == joltage
            for i, joltage in enumerate(joltages)
        ]
        s.add(z3.And(constraints))

        # solve
        s.minimize(sum(presses))
        s.check()

        # collect results
        m = s.model()
        min_presses = sum(m[sol].as_long() for sol in m)
        answer_presses.append(min_presses)
    return sum(answer_presses)


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    machines = read_input(args.filename)
    print(f"Part1: {part1(machines)}")
    print(f"Part2: {part2(machines)}")
