import gleam/result
import simplifile
import day01_calorie_counting
import gleeunit
import gleeunit/should

pub fn main() {
  gleeunit.main()
}

fn get_example_input() -> List(List(Int)) {
  "../example.txt"
  |> simplifile.read()
  |> result.unwrap(or: "Error reading file")
  |> day01_calorie_counting.parse_input
}

pub fn part1_test() {
  get_example_input()
  |> day01_calorie_counting.part1
  |> should.equal(24000)
}

pub fn part2_test() {
  get_example_input()
  |> day01_calorie_counting.part2
  |> should.equal(45000)
}