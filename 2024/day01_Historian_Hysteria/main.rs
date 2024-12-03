use std::collections::HashMap;
use std::{env, fs};

fn read_input(filename: &str) -> (Vec<u32>, Vec<u32>) {
    fs::read_to_string(filename).expect("Unable to open file")
        .lines()
        .map(|line| {
            let parts: Vec<_> = line.split_whitespace().collect();
            let l = parts[0].parse::<u32>().unwrap();
            let r = parts[1].parse::<u32>().unwrap();
            (l, r)
        })
        .unzip()
}

fn part1(left: &[u32], right: &[u32]) -> u32 {
    left.iter().zip(right.iter())
        .map(|(l, r)| l.abs_diff(*r))
        .sum()
}

fn part2(left: &[u32], right: &[u32]) -> u32 {
    let mut right_ct = HashMap::new();

    for &r in right {
        *right_ct.entry(r).or_insert(0) += 1;
    }

    left.iter()
        .map(|&l| l * *right_ct.get(&l).unwrap_or(&0))
        .sum()
}

fn main() {
    let mut filename = "input.txt";
    let args: Vec<String> = env::args().collect();
    if args.len() == 2 {
        filename = &args[1];
    }

    let (mut left, mut right) = read_input(filename);
    left.sort();
    right.sort();

    println!("Part1: sort_dist = {}", part1(&left, &right));
    println!("Part2: similarity_score = {}", part2(&left, &right));
}
