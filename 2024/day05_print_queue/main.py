import argparse
from collections import defaultdict


def read_input(filename):
    rules = defaultdict(list)
    updates = list()
    with open(filename, 'r') as file:
        parse_step = 1
        for line in file:
            line = line.strip()
            if line == "":
                parse_step = 2
                continue

            match parse_step:
                case 1:  # Parse rules
                    parts = line.split("|")
                    rules[int(parts[0])].append(int(parts[1]))
                case 2:  # Parse report pages
                    updates.append(list(map(int, line.split(","))))

    return rules, updates


def is_valid_order(rules, pages):
    invalid_pages = set()
    for p in pages[::-1]:
        if p in invalid_pages:
            return False
        invalid_pages.update(rules[p])
    return True


def reorder_pages(rules, pages):
    edges = defaultdict(list)

    # Create a list of edges that only contains the other pages in this report
    for p in pages:
        edges[p] = list(filter(lambda r: r in pages, rules[p]))

    # Since the rules always describe an unambigious order, we can
    # just sort by length of requirements to get the proper order
    return sorted(edges, key=lambda key: len(edges[key]))


def solve(rules, updates):
    sum_mid_pages = 0
    sum_mid_invalid_pages = 0
    invalid_update_inds = []

    # Part 1
    for ind, update in enumerate(updates):
        if is_valid_order(rules, update):
            sum_mid_pages += update[int(len(update)/2)]
        else:
            invalid_update_inds.append(ind)

    # Part 2
    for ind in invalid_update_inds:
        reordered = reorder_pages(rules, updates[ind])
        sum_mid_invalid_pages += reordered[int(len(reordered)/2)]
    return sum_mid_pages, sum_mid_invalid_pages


if __name__ == '__main__':
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("filename", nargs='?',
                        help="input filename", default="input.txt")
    args = parser.parse_args()

    rules, updates = read_input(args.filename)
    sum_mid_pages, sum_mid_invalid_pages = solve(rules, updates)

    print(f"\nPart1: sum_mid_pages = {sum_mid_pages}")
    print(f"Part2: sum_mid_invalid_pages = {sum_mid_invalid_pages}\n")
