# Day 3: Mull it Over

https://adventofcode.com/2024/day/3

## Part 1

Sum all occurences of multiplications indicated by `mul(\d{1,3},\d{1,3})` in input

#### Example:

```
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
```

Answer: (2\*4 + 5\*5 + 11\*8 + 8\*5) = `161`

## Part 2

Same as part 1, but skip any multiplications between `don't()` and `do()`

#### Example:

```
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
```

Answer: (2\*4 + 8\*5) = `48`
