import argparse
from collections import deque
from cpu import CPU


def read_input(filename):
    with open(filename, 'r') as file:
        a = int(file.readline().split(":")[1].strip())
        b = int(file.readline().split(":")[1].strip())
        c = int(file.readline().split(":")[1].strip())
        file.readline()
        prog = list(map(int, file.readline().split(" ")[1].split(",")))
        return a, b, c, prog


def run_program(a, b, c, prog):
    """ Part 1  """
    cpu = CPU(a, b, c, prog)
    cpu.run()
    return list(map(int, cpu.OUTPUT))


def find_quine_iterative_backtrack(prog):
    """ Part 2 (iterative) """
    queue = deque()
    queue.append((0, 1))

    while queue:
        a, n = queue.popleft()
        if n > len(prog):  # Base
            return a

        for i in range(8):
            a2 = (a << 3) | i
            out = run_program(a2, 0, 0, prog)
            target = prog[-n:]

            # save correct partial solutions
            if out == target:
                queue.append((a2, n + 1))
    return False


def find_quine_recursive_backtrack(prog, a, n):
    """ Part 2 (recursive) """
    if n > len(prog):  # Base
        return a
    for i in range(8):
        a2 = (a << 3) | i
        out = run_program(a2, 0, 0, prog)
        target = prog[-n:]
        if out == target:
            res = find_quine_recursive_backtrack(prog, a2, n+1)
            if res:
                return res
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    a, b, c, prog = read_input(args.filename)

    p1 = ','.join(map(str, run_program(a, b, c, prog)))
    print(f"\nPart1: p1 = {p1}")

    p2 = find_quine_iterative_backtrack(prog)
    print(f"Part2: p2_iterative = {p2}")

    p2 = find_quine_recursive_backtrack(prog, 0, 1)
    print(f"Part2: p2_recursive = {p2}")
