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
    _ -> "input.txt"
  }
}

pub fn parse_input(contents: String) -> List(#(String, String)) {
  contents
  |> string.trim()
  |> string.split("\n")
  |> list.map(fn(game) {
    case string.split(game, " ") {
      [first, second] -> #(first, second)
      _ -> panic as "Invalid game input"
    }
  })
}

fn play_game(game: #(String, String)) -> Int {
  case game {
    #("A", "X") -> 3 + 1
    #("A", "Y") -> 6 + 2
    #("A", "Z") -> 0 + 3
    #("B", "X") -> 0 + 1
    #("B", "Y") -> 3 + 2
    #("B", "Z") -> 6 + 3
    #("C", "X") -> 6 + 1
    #("C", "Y") -> 0 + 2
    #("C", "Z") -> 3 + 3
    _ -> 0
  }
}

fn determine_move(game: #(String, String)) -> #(String, String) {
  let #(first, _) = game
  case game {
    #("A", "X") -> #(first, "Z")
    #("A", "Y") -> #(first, "X")
    #("A", "Z") -> #(first, "Y")
    #("B", "X") -> #(first, "X")
    #("B", "Y") -> #(first, "Y")
    #("B", "Z") -> #(first, "Z")
    #("C", "X") -> #(first, "Y")
    #("C", "Y") -> #(first, "Z")
    #("C", "Z") -> #(first, "X")
    _ -> panic as "Invalid game"
  }
}

pub fn part1(games: List(#(String, String))) -> Int {
  games
  |> list.map(play_game)
  |> list.fold(0, int.add)
}

pub fn part2(games: List(#(String, String))) -> Int {
  games
  |> list.map(determine_move)
  |> list.map(play_game)
  |> list.fold(0, int.add)
}

pub fn main() {
  let games =
    get_filename()
    |> simplifile.read()
    |> result.unwrap("Error reading file")
    |> parse_input

  io.println("Part1: " <> int.to_string(part1(games)))
  io.println("Part2: " <> int.to_string(part2(games)))
}
