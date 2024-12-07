use std::fs;

fn parse_digits(t_num: &str) -> Vec<u32> {
    t_num
        .chars()
        .filter_map(|a| a.to_digit(10))
        .collect()
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("couldn't read input file");
    let lines: Vec<String> = input.lines().map(String::from).collect();
    let mut total: u32 = 0;

    for l in lines {
        // Remove all non-numerics
        let clean = parse_digits(&l);
        let total_str = format!("{}{}", clean[0], clean[clean.len()-1]);
        total += total_str.parse::<u32>().unwrap();
    }
    println!("Sum: {}", total);
}
