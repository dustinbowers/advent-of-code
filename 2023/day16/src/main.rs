fn parse_input(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .collect::<Vec<&str>>()
        .iter()
        .map(|s| s.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>()
}
fn print_board(board : &Vec<Vec<char>>) {
    board.iter().for_each(|r| {
        println!("{}", r.into_iter().collect::<String>());
    });
}

fn part1(input : &str) {
    let mut board = parse_input(&input);
    let mut board_state : Vec<Vec<State>> = vec![];
    for r in &board {
        board_state.push(vec![State::None; r.len()]);
    }

    propagate_beam(&mut board, &mut board_state, 0, 0, Direction::Right);

    print_board(&board);

}
#[derive(Clone)]
enum State{
    Energized,
    None
}
enum Direction {
    Up,
    Down,
    Left,
    Right
}
fn propagate_beam(board : &mut Vec<Vec<char>>, board_state : &mut Vec<Vec<State>>, row : usize, col : usize, direction : Direction) {
    let mut r = row as i32;
    let mut c = col as i32;
    let max_r = board.len() as i32;
    let max_c = board[0].len() as i32;
    while board[r as usize][c as usize] == '.' || board[r as usize][c as usize] == '#'{
        match direction {
            Direction::Up => r -= 1,
            Direction::Down => r += 1,
            Direction::Left => c -= 1,
            Direction::Right => c += 1,
        }
        if r < 0 || c < 0 || r > max_r || c > max_c {
            return
        }
    }
}

fn main() {
    let input_filename = "input_example.txt";
    let input = std::fs::read_to_string(&input_filename).expect("File not found");

    part1(&input);
}
