# Day 2: Red-Nosed Reports

https://adventofcode.com/2024/day/2

## Part 1

Each line is a "report" with "level" values. Return count of "safe" reports
**Safe reports**:

- The levels are either all **increasing** or all **decreasing**.
- Any two adjacent levels **differ by at least one and at most three**.

#### Example:

```
7 6 4 2 1 // safe
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9 // safe
```

Answer: 2

## Part 2

Same as part 1, but allow up to 1 "level" value to be removed in order to make a report safe

#### Example:

```
7 6 4 2 1 // safe
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5 // safe
8 6 4 4 1 // safe
1 3 6 7 9 // safe
```

Answer: 4
