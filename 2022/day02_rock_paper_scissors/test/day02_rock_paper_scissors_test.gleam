import day02_rock_paper_scissors
import gleam/result
import gleeunit
import gleeunit/should
import simplifile

pub fn main() {
  gleeunit.main()
}

// gleeunit test functions end in `_test`
pub fn hello_world_test() {
  1
  |> should.equal(1)
}

fn get_example_input() -> List(#(String, String)) {
  "example.txt"
  |> simplifile.read()
  |> result.unwrap(or: "Error reading file")
  |> day02_rock_paper_scissors.parse_input
}

pub fn part1_test() {
  get_example_input()
  |> day02_rock_paper_scissors.part1
  |> should.equal(15)
}

pub fn part2_test() {
  get_example_input()
  |> day02_rock_paper_scissors.part2
  |> should.equal(12)
}
