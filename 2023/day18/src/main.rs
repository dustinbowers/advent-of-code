
#[derive(Debug)]
enum Direction {
    None,
    Up,
    Down,
    Left,
    Right,
}
fn parse_input(input : &str) -> Vec<(Direction , i32)> {
    input.lines().map(|line| {
        let parts = line.split_whitespace().collect::<Vec<&str>>();
        let dir : Direction = match parts[0] {
            "U" => Direction::Up,
            "D" => Direction::Down,
            "L" => Direction::Left,
            "R" => Direction::Right,
            _ => Direction::None,
        };
        let dist : i32 = (parts[1]).parse().unwrap();
        (dir, dist)
    }).collect()
}

fn part1(input : &str) {
    let lines = parse_input(&input);
    // println!("Directions:\n{:#?}", lines);
    let mut left = 0;
    let mut right = 0;
    let mut top = 0;
    let mut bottom = 0;
    let mut curr_i = 0;
    let mut curr_j = 0;

    for (dir, dist) in lines {
        match dir {
            Direction::Up => {
                curr_i -= dist;
                if curr_i < top {
                    top = curr_i;
                }
            },
            Direction::Down => {
                curr_i += dist;
                if curr_i > bottom {
                    bottom = curr_i;
                }
            },
            Direction::Left => {
                curr_j -= dist;
                if curr_j < left {
                    left = curr_j;
                }
            },
            Direction::Right => {
                curr_j += dist;
                if curr_j > right {
                    right = curr_j;
                }
            }
            Direction::None => {},
        };
    }
    let height = bottom - top + 1;
    let width = right - left + 1;
    println!("Top-Left = ({}, {})\nBottom-right = ({}, {})\nwidth = {}, height = {}", top, left, bottom, right, width, height);

    let lagoon : Vec<Vec<i32>> = [0..height].iter().map(|i| {
        return vec![i; width as usize];
    }).collect();

    println!("Lagoon:");
    for r in lagoon {
        println!("{:?}", r);
    }

}

fn main() {
    let input_filename = "input_example.txt";
    // let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found");

    part1(&input);
}
