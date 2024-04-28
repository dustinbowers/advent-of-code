use std::collections::HashMap;

#[derive(Debug, Eq, PartialEq)]
enum Direction {
    Up,
    Down,
    Left,
    Right,
}

fn get_piece_map() -> HashMap<char, Vec<Direction>> {
    HashMap::<char, Vec<Direction>>::from([
        ('|', vec![Direction::Up, Direction::Down]),
        ('-', vec![Direction::Left, Direction::Right]),
        ('L', vec![Direction::Up, Direction::Right]),
        ('J', vec![Direction::Up, Direction::Left]),
        ('7', vec![Direction::Down, Direction::Left]),
        ('F', vec![Direction::Down, Direction::Right]),
    ])
}

fn parse_maze(input: &str) -> (Vec<Vec<char>>, Vec<Vec<Option<i32>>>, usize, usize) {
    let mut maze: Vec<Vec<char>> = vec![];
    let mut walked: Vec<Vec<Option<i32>>> = vec![];

    let mut start_i = 0;
    let mut start_j = 0;

    for (i, line) in input.lines().enumerate() {
        maze.push(vec![]);
        walked.push(vec![]);
        for (j, c) in line.chars().enumerate() {
            maze[i].push(c);
            match c {
                '|' | '-' | 'L' | 'J' | '7' | 'F' => {}
                _ => {}
            }
            walked[i].push(None);
            if c == 'S' {
                start_i = i;
                start_j = j;
            }
        }
    }
    (maze, walked, start_i, start_j)
}
fn determine_starting_piece(
    maze: &Vec<Vec<char>>,
    pieces: &HashMap<char, Vec<Direction>>,
    start_i: &usize,
    start_j: &usize,
) -> char {
    // Determine what S is based on its neighbors
    let i = start_i;
    let j = start_j;

    let mut inbound_pipes: Vec<Direction> = vec![];
    if (*i as i32) - 1 > 0 && maze[i - 1][*j] != '.' {
        let dirs = pieces.get(&maze[i - 1][*j]).unwrap();
        if dirs.contains(&Direction::Down) {
            inbound_pipes.push(Direction::Up);
        }
    }
    if i + 1 < maze.len() && maze[i + 1][*j] != '.' {
        let dirs = pieces.get(&maze[i + 1][*j]).unwrap();
        if dirs.contains(&Direction::Up) {
            inbound_pipes.push(Direction::Down);
        }
    }
    if (*j as i32) - 1 > 0 && maze[*i][j - 1] != '.' {
        let dirs = pieces.get(&maze[*i][j - 1]).unwrap();
        if dirs.contains(&Direction::Right) {
            inbound_pipes.push(Direction::Left);
        }
    }
    if j + 1 < maze.len() && maze[*i][j + 1] != '.' {
        let dirs = pieces.get(&maze[*i][j + 1]).unwrap();
        if dirs.contains(&Direction::Left) {
            inbound_pipes.push(Direction::Right);
        }
    }
    println!("inbound pipes = {:?}", inbound_pipes);
    for (_, directions) in pieces.iter().enumerate() {
        if &inbound_pipes == directions.1 {
            println!("found piece! {}", directions.0);
            //maze[start_i][start_j] = *directions.0;
            return *directions.0;
        }
    }
    ' '
}

fn walk_maze(
    maze: &Vec<Vec<char>>,
    mut walked: &mut Vec<Vec<Option<i32>>>,
    pieces: &HashMap<char, Vec<Direction>>,
    start_i: usize,
    start_j: usize,
) -> (Vec<Vec<Option<i32>>>, i32) {
    // Walk the maze
    let mut idx = 0;
    let mut curr_i = start_i;
    let mut curr_j = start_j;
    walked[curr_i][curr_j] = Some(idx);
    idx += 0;
    let mut is_done = false;
    let mut c = 0;
    while !is_done {
        c += 1;
        println!(
            "c = {}, idx = {}, curr pos ({}, {})",
            c, idx, curr_i, curr_j
        );
        let directions = pieces.get(&maze[curr_i][curr_j]).unwrap();
        println!(
            "Walking '{}', Directions = {:?}",
            &maze[curr_i][curr_j], directions
        );
        for d in directions {
            let mut next_i = curr_i;
            let mut next_j = curr_j;

            if *d == Direction::Up {
                next_i -= 1;
            } else if *d == Direction::Down {
                next_i += 1;
            }
            if *d == Direction::Left {
                next_j -= 1;
            } else if *d == Direction::Right {
                next_j += 1;
            }

            println!(
                "Direction = {:?}. Next position ({},{}) == {:?}",
                d, next_i, next_j, walked[next_i][next_j]
            );
            if walked[next_i][next_j] == None {
                walked[curr_i][curr_j] = Some(idx);
                idx += 1;
                curr_i = next_i;
                curr_j = next_j;
                break;
            }
            if walked[next_i][next_j] == Some(0) && idx > 1 {
                is_done = true;
                walked[curr_i][curr_j] = Some(idx);
                break;
            }
        }
    }
    (walked.to_vec(), idx)
}

fn part1(
    input: &str,
) -> (
    Vec<Vec<char>>,
    Vec<Vec<Option<i32>>>,
    HashMap<char, Vec<Direction>>,
) {
    let pieces = get_piece_map();
    let (mut maze, mut walked, start_i, start_j) = parse_maze(&input);
    let starting_piece = determine_starting_piece(&maze, &pieces, &start_i, &start_j);
    maze[start_i][start_j] = starting_piece;

    println!("Starting position ({}, {})", start_i, start_j);
    print_maze(&maze);
    let (walked, idx) = walk_maze(&maze, &mut walked, &pieces, start_i, start_j);
    print_walked(&walked);

    println!("Max distance = {}", idx / 2 + 1);

    (maze, walked, pieces)
}

fn print_maze(maze: &Vec<Vec<char>>) {
    for r in maze {
        println!("{:?}", r);
    }
}

fn print_walked(walked: &Vec<Vec<Option<i32>>>) {
    for r in walked {
        for c in r {
            match c {
                Some(t) => {
                    print!("{}", t);
                }
                None => {
                    print!(".");
                }
            }
        }
        println!();
    }
}

fn clean_maze<'a>(
    maze: &'a mut Vec<Vec<char>>,
    walked: &'a Vec<Vec<Option<i32>>>,
) -> &'a mut Vec<Vec<char>> {
    for (i, line) in maze.iter_mut().enumerate() {
        for (j, c) in line.iter_mut().enumerate() {
            match walked[i][j] {
                Some(n) => {}
                None => {
                    *c = '.';
                }
            }
        }
    }
    maze
}

fn part2(input: &str) {
    let (mut maze, walked, pieces) = part1(input);
    let maze = clean_maze(&mut maze, &walked);

    let mut inside_ct = 0;
    for (i, line) in maze.iter().enumerate() {
        let mut parity_line: Vec<i32> = vec![];
        let mut parity = 0;
        let mut last_corner: char = ' ';
        for (j, c) in line.iter().enumerate() {
            parity_line.push(parity);
            if *c == '-' {
                continue;
            }
            if *c == 'F' || *c == 'L' {
                last_corner = *c;
                continue;
            }
            // If NOT a U-shape, then it must be a region-separator
            if (last_corner == 'F' && *c == 'J') || (last_corner == 'L' && *c == '7') {
                parity += 1;
                last_corner = ' ';
                continue;
            }
            if *c == '|' {
                parity += 1;
                continue;
            }
            if *c == '.' {
                if parity % 2 == 1 {
                    inside_ct += 1;
                }
            }
        }
        println!(
            "line = {:?}\tparity_line = {:?}\tinside_ct = {}",
            line, parity_line, inside_ct
        );
    }
    println!("Inside cells = {}", inside_ct);
}

fn main() {
    let input_filename = "input_example3.txt";
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found");

    // part1(&input);
    part2(&input); // 595
}
