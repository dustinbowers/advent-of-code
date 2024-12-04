#![feature(array_windows)]
use std::{env, fs};

fn is_safe(report: &[i32]) -> bool {
    let mut c = 1;
    if report[1] - report[0] < 0 {
        c = -1;
    }
    for i in 1..report.len() {
        let v = c * (report[i] - report[i-1]);
        if v < 1 || v > 3 {
            return false
        }
    }
    true
}

fn solve(reports: &Vec<Vec<i32>>) -> (i32, i32) {
    let mut safe_ct = 0;
    let mut safe_ct_with_dampening = 0;
    for report in reports {
        if is_safe(&report) {
            safe_ct += 1;
        } else {
            for i in 0..report.len() {
                let mut dampened_report = report.clone();
                dampened_report.remove(i);
                if is_safe(&dampened_report) {
                    safe_ct_with_dampening += 1;
                    break;
                }
            }
        }
    }
    (safe_ct, safe_ct + safe_ct_with_dampening)
}
fn read_input(filename: &str) -> Vec<Vec<i32>> {
    fs::read_to_string(filename).expect("Unable to open file")
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|v| v.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
        }).collect()
}

fn main() {
    let mut filename = "input.txt";
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 {
        filename = &args[1];
    }

    let reports = read_input(filename);
    let (safe_ct, safe_ct_with_dampening) = solve(&reports);
    println!("Part1: safe_ct = {}", safe_ct);
    println!("Part2: safe_ct_with_dampening = {}", safe_ct_with_dampening);
}
