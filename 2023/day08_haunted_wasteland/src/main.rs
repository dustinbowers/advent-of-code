use regex::Regex;
use std::collections::HashMap;

fn generate_map(input: &str) -> (Vec<char>, HashMap<String, (String, String)>) {
    let lines = input.lines().collect::<Vec<&str>>();
    let directions = lines[0].chars().collect::<Vec<_>>();
    let mut map: HashMap<String, (String, String)> = HashMap::new();
    let map_regex: Regex = Regex::new(r"(?<target>.+) = \((?<left>.+), (?<right>.+)\)").unwrap();
    for m in &lines[2..] {
        let Some(caps) = map_regex.captures(m) else {
            continue;
        };
        map.insert(
            caps["target"].to_owned(),
            (caps["left"].to_owned(), caps["right"].to_owned()),
        );
    }
    (directions, map)
}
fn part1(input: &str) {
    let (directions, map) = generate_map(input);
    println!("map = {:?}", map);

    // Repeatedly follow the directions until we reach "ZZZ"
    let dir_len = directions.len();
    let mut current = "AAA";
    let mut i = 0;
    while current != "ZZZ" {
        let c = map.get(current).unwrap();
        let d = directions[i % dir_len];
        i += 1;
        match d {
            'L' => current = &c.0,
            'R' => current = &c.1,
            _ => {}
        }
    }
    println!("Steps taken = {}", i);
}

fn part2(input: &str) {
    let (directions, map) = generate_map(input);
    println!("map = {:?}", map);

    let mut current_nodes: Vec<String> = vec![];
    // Find all starting nodes that end with 'A'
    for t in map.keys() {
        if t.ends_with("A") {
            current_nodes.push(t.to_owned());
        }
    }
    println!("Starting nodes: {:?}", current_nodes);

    // Find the cycle_length of each starting node
    let dir_len = directions.len();
    let mut cycle_length = vec![];
    for cn in current_nodes {
        let mut n = cn;
        let mut cycle_len = 0;
        while !n.ends_with("Z") {
            let d = directions[cycle_len % dir_len];
            let next_node = map.get(&n).unwrap();
            match d {
                'L' => {
                    n = next_node.0.clone();
                }
                'R' => {
                    n = next_node.1.clone();
                }
                _ => {}
            }
            cycle_len += 1;
        }
        println!("Cycle length = {}", cycle_len);
        cycle_length.push(cycle_len);
    }

    let l = lcm(&cycle_length);

    println!("All nodes end at Z. Steps taken = {}", l);
}

pub fn lcm(nums: &[usize]) -> usize {
    if nums.len() == 1 {
        return nums[0];
    }
    let a = nums[0];
    let b = lcm(&nums[1..]);
    a * b / gcd_of_two_numbers(a, b)
}

fn gcd_of_two_numbers(a: usize, b: usize) -> usize {
    if b == 0 {
        return a;
    }
    gcd_of_two_numbers(b, a % b)
}

fn main() {
    let input_file = "input_test.txt";
    let input = std::fs::read_to_string(input_file).unwrap();

    part1(&input);
    part2(&input);
}
