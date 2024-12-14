use std::fs::File;
use std::io::{self, BufRead};
use std::path::Path;
use std::time::Instant;

fn find_ab(ax: i64, ay: i64, bx: i64, by: i64, mut px: i64, mut py: i64, unit_conversion_error: bool) -> Option<i64> {

    let det = ax * by - bx * ay;
    if det == 0 {
        return None;
    }

    if unit_conversion_error {
        px += 10000000000000;
        py += 10000000000000;
    }

    let det_a = px * by - bx * py;
    if det_a % det != 0 {
        return None;
    }

    let det_b = ax * py - px * ay;
    if det_b % det != 0 {
        return None;
    }

    let a = det_a / det;
    let b = det_b / det;

    return Some(a * 3 + b);
}

fn solve(filename: &str) -> (i64, i64) {
    let path = Path::new(filename);
    let file = File::open(&path).expect("can't read file");
    let lines = io::BufReader::new(file).lines();

    let mut lines_iter = lines.filter_map(|line| line.ok()).peekable();

    let mut p1_total = 0i64;
    let mut p2_total = 0i64;
    while lines_iter.peek().is_some() {
        // Parse button A
        if let Some(button_a_line) = lines_iter.next() {
            let (_, coords) = button_a_line.split_once(": ").unwrap();
            let (ax_str, ay_str) = coords.split_once(", ").unwrap();
            let ax = ax_str[2..].parse::<i64>().unwrap();
            let ay = ay_str[2..].parse::<i64>().unwrap();

            // Parse button B
            let button_b_line = lines_iter.next().unwrap();
            let (_, coords) = button_b_line.split_once(": ").unwrap();
            let (bx_str, by_str) = coords.split_once(", ").unwrap();
            let bx = bx_str[2..].parse::<i64>().unwrap();
            let by = by_str[2..].parse::<i64>().unwrap();

            // Parse prize
            let prize_line = lines_iter.next().unwrap();
            let (_, coords) = prize_line.split_once(": ").unwrap();
            let (px_str, py_str) = coords.split_once(", ").unwrap();
            let px = px_str[2..].parse::<i64>().unwrap();
            let py = py_str[2..].parse::<i64>().unwrap();

            // solve p1
            if let Some(p1) = find_ab(ax, ay, bx, by, px, py, false) {
                p1_total += p1;
            }
            // solve p2
            if let Some(p2) = find_ab(ax, ay, bx, by, px, py, true) {
                p2_total += p2;
            }
        }
        lines_iter.next();
    }

    (p1_total, p2_total)
}

fn main() {
    let start = Instant::now();
    let (p1, p2) = solve("input.txt");
    let duration = start.elapsed();

    print!("Part1: {}\nPart2: {}\n", p1, p2);
    println!("Execution time: {:?}", duration);
}


