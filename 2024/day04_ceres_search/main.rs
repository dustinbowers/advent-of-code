use std::{env, fs};

fn read_input(filename: &str) -> Vec<Vec<char>> {
    fs::read_to_string(filename).expect("Unable to open file")
        .lines()
        .map(|line| line.chars().collect())
        .collect()
}

const DIRECTIONS: &[(i32, i32)] = &[
    (-1, -1), (0, -1), (1, -1),
    (-1,  0),          (1,  0),
    (-1,  1), (0,  1), (1,  1),
];

fn part1(input: &Vec<Vec<char>>) -> u32 {
    let mut xmas_ct = 0u32;
    for (r, row) in input.iter().enumerate() {
        for (c, &cell) in row.iter().enumerate() {
            if cell == 'X' {
                for d in DIRECTIONS {
                    let mut x = r as i32;
                    let mut y = c as i32;
                    let mut s = String::new();
                    for _ in 0..4 {
                        if x < 0 || y < 0 || x >= input.len() as i32 || y >= row.len() as i32 {
                            break;
                        }
                        s.push(input[x as usize][y as usize]);
                        x += d.0;
                        y += d.1;
                    }
                    if s == "XMAS" {
                        xmas_ct += 1;
                    }
                }
            }
        }
    }
    xmas_ct
}

fn part2(input: &Vec<Vec<char>>) -> u32 {
    let mut mas_ct = 0;
    for r in 1..input.len()-1 {
        for c in 1..input[0].len()-1 {
            if input[r][c] == 'A' {
                let nw = input[r-1][c-1];
                let se = input[r+1][c+1];
                let ne = input[r+1][c-1];
                let sw = input[r-1][c+1];
                let diag = format!("{nw}{se}");
                let anti_diag = format!("{ne}{sw}");
                if (diag == "MS" || diag == "SM") && (anti_diag == "MS" || anti_diag == "SM") {
                    mas_ct += 1;
                }
            }
        }
    }
    mas_ct
}

fn main() {
    let mut filename = "input.txt";
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 {
        filename = &args[1];
    }

    let input = read_input(filename);
    let xmas_ct = part1(&input);
    let mas_ct = part2(&input);

    println!("Part1: xmas_count = {}", xmas_ct);
    println!("Part1: mas_count = {}", mas_ct);
}

