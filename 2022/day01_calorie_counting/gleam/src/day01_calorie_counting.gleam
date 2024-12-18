import argv
import gleam/int
import gleam/io
import gleam/list
import gleam/result
import gleam/string
import simplifile

pub fn get_filename() -> String {
  case argv.load().arguments {
    [filename] -> filename
    _ -> "../input.txt"
  }
}

pub fn parse_input(contents: String) -> List(List(Int)) {
  contents
  |> string.split("\n\n")
  |> list.map(fn(group) {
    group
    |> string.trim()
    |> string.split("\n")
    |> list.filter_map(int.parse)
  })
}

fn sum_group(elf: List(Int)) -> Int {
  elf |> list.fold(0, int.add)
}

pub fn part1(elves: List(List(Int))) -> Int {
  elves
  |> list.map(sum_group)
  |> list.fold(0, int.max)
}

pub fn part2(elves: List(List(Int))) -> Int {
  elves
  |> list.map(sum_group)
  |> list.sort(by: int.compare)
  |> list.reverse()
  |> list.take(3)
  |> list.fold(0, int.add)
}

pub fn main() {
  let elves =
    get_filename()
    |> simplifile.read()
    |> result.unwrap(or: "Error reading file")
    |> parse_input

  io.println("Part 1: " <> int.to_string(part1(elves)))
  io.println("Part 2: " <> int.to_string(part2(elves)))
}
