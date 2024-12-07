use regex::Regex;

fn parse_input(input: &str) -> Vec<&str> {
    input.split(",").collect()
}
fn hash_str(s: &str) -> u32 {
    s.chars()
        .fold(0u32, |acc, c| ((acc + (c as u32)) * 17) % 256)
}
fn part1(input: &str) {
    let total = parse_input(input)
        .iter()
        .fold(0, |acc, t| acc + hash_str(t));
    println!("Part 1 total = {}", total);
}
fn part2(input: &str) {
    let mut boxes: Vec<Vec<(String, String)>> = vec![vec![]; 256];
    let kv_regex = Regex::new(r"(?<key>[a-zA-Z]+)(?<op>[-=])(?<val>.*)?").unwrap();

    parse_input(input).iter().for_each(|t| {
        let Some(caps) = kv_regex.captures(t) else {
            panic!("bad token");
        };
        let key = caps["key"].to_owned();
        let op = caps["op"].to_owned();
        let val = caps["val"].to_owned();

        let h = hash_str(&key) as usize;
        if op == "=" {
            let mut update_ind = None;
            for (i, bucket) in boxes[h].iter().enumerate() {
                if bucket.0 == key {
                    update_ind = Some(i);
                    break;
                }
            }
            match update_ind {
                Some(ind) => boxes[h][ind] = (key.clone(), val.clone()), // update
                None => boxes[h].push((key.clone(), val.clone())),       // insert
            };
        } else if op == "-" {
            boxes[h].retain(|(k, _)| *k != key) // remove
        }
    });
    println!("Part 2, focusing power = {}", calc_focusing_power(boxes));
}
fn calc_focusing_power(boxes: Vec<Vec<(String, String)>>) -> usize {
    boxes
        .iter()
        .enumerate()
        .map(|(i, b)| {
            b.iter().enumerate().fold(0, |acc, (j, t)| {
                acc + (i + 1) * (j + 1) * t.1.parse::<usize>().unwrap()
            })
        })
        .sum()
}

fn main() {
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found");
    part1(&input);
    part2(&input);
}
