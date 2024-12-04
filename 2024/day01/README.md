# Day 1: Historian Hysteria

https://adventofcode.com/2024/day/1

## Part 1

Sort each column, then sum the absolute difference of the parallel arrays

#### Example:

```
3   4
4   3
2   5
1   3
3   9
3   3
```
Answer: 2 + 1 + 0 + 1 + 2 + 5 = `11`

## Part 2

For each element in left column, multiply the value of the element by the count of that element in right column

#### Example:
```
3   4
4   3
2   5
1   3
3   9
3   3
```
Answer: (3\*3 + 4\*1 + 2\*0 + 1\*0 + 3\*3 + 3\*3) = `31`
