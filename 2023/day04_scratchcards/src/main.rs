use std::collections::HashMap;

fn get_card_matches(game_line: &str) -> (u32, u32) {
    let parts: Vec<&str> = game_line.split(": ").collect();
    let card_str: String = parts[0].chars().filter(|c| c.is_digit(10)).collect();
    let card_num = card_str.parse::<u32>().unwrap();
    let nums: Vec<_> = parts[1].split(" | ").collect();
    let winning_nums = nums[0];
    let game_nums = nums[1];

    let mut winning_map: HashMap<u32, ()> = HashMap::new();
    for n in winning_nums.split_whitespace().collect::<Vec<_>>() {
        let w = n.parse::<u32>().unwrap();
        winning_map.insert(w, ());
    }

    let mut matched_numbers = 0u32;
    for n in game_nums.split_whitespace().collect::<Vec<_>>() {
        let k = n.parse::<u32>().unwrap();
        if winning_map.contains_key(&k) {
            matched_numbers += 1;
        }
    }

    (card_num, matched_numbers)
}
fn part1(input: &str) {
    let mut total_score = 0u32;
    let lines: Vec<String> = input.lines().map(String::from).collect();
    for l in &lines {
        println!("Parsing line: {}", l);
        let (_, matched_numbers) = get_card_matches(l);
        let mut card_score = 0u32;
        if matched_numbers > 0 {
            card_score = 1 << (matched_numbers - 1);
        }
        println!("Current card score: {}", card_score);
        total_score += card_score;
    }
    println!("\nPart 1 Total score: {}", total_score);
}

fn part2(input: &str) {
    let mut card_counts: HashMap<u32, u32> = HashMap::new();
    let lines: Vec<String> = input.lines().map(String::from).collect();
    for l in &lines {
        println!("Parsing line: {}", l);
        let (card_num, matched_numbers) = get_card_matches(l);
        if !card_counts.contains_key(&card_num) {
            card_counts.insert(card_num, 1u32);
        }
        let current_copies = *card_counts.get(&card_num).unwrap();
        println!(
            "We have {} copies of Card {}, it has {} matches.",
            current_copies, card_num, matched_numbers
        );
        for i in 1..=matched_numbers {
            let winning_idx = card_num + i;
            if !card_counts.contains_key(&winning_idx) {
                card_counts.insert(winning_idx, 1);
            }
            card_counts.insert(
                winning_idx,
                card_counts.get(&winning_idx).unwrap() + current_copies,
            );
            println!(
                " - Adding {} copies to {}. Total count now = {}",
                current_copies,
                winning_idx,
                card_counts.get(&winning_idx).unwrap()
            );
        }
    }
    let mut total = 0;
    for i in 1..=card_counts.len() as u32 {
        let copies = card_counts.get(&i).unwrap();
        println!("card {}: {} copies", i, copies);
        total += *copies;
    }
    println!("Total copies = {}", total);
}

fn main() {
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found");
    part1(&input);
    part2(&input);
}
