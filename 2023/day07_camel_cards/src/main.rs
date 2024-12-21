use std::collections::HashMap;

#[derive(Debug)]
struct Hand {
    hand_strength: u64,
    bid: u32,
}
fn calc_hand_strength(hand: &str, rank: u32) -> u64 {
    let mut str = 0u64;
    let card_ranks: HashMap<char, u32> = HashMap::from([
        ('2', 1),
        ('3', 2),
        ('4', 3),
        ('5', 4),
        ('6', 5),
        ('7', 6),
        ('8', 7),
        ('9', 8),
        ('T', 9),
        ('J', 0), //('J', 10),
        ('Q', 11),
        ('K', 12),
        ('A', 13),
    ]);
    for (i, c) in hand.chars().enumerate() {
        let r = card_ranks.get(&c).unwrap();
        let j = i as u64;

        // Get JANKY with these hand-strength sums
        str += (16u64 - (j * 3)).pow(5 - j as u32) * (*r as u64);
    }
    str += 100_000_000 * (rank as u64);
    str
}
fn part2(input: &str) {
    let mut hands: Vec<Hand> = vec![];

    for l in input.lines() {
        let (hand, bid) = parse_line(l);

        let rank = rank_hand(&hand);

        hands.push(Hand {
            hand_strength: calc_hand_strength(hand, rank),
            bid: bid,
        });
    }

    hands.sort_by_key(|h| h.hand_strength);

    let mut total = 0u64;
    for (i, h) in hands.iter().enumerate() {
        println!("Hand: {:?}", h);
        total += (i + 1) as u64 * (h.bid as u64);
    }

    println!("Part 1, bid sum: {}", total);
}

fn rank_hand(hand: &str) -> u32 {
    let mut jokers = 0;

    let mut cards: HashMap<char, u32> = HashMap::new();
    for c in hand.chars() {
        if c == 'J' {
            jokers += 1;
            continue;
        }
        if !cards.contains_key(&c) {
            cards.insert(c, 1);
        } else {
            cards.insert(c, cards.get(&c).unwrap() + 1);
        }
    }
    let mut counts: Vec<_> = cards.values().cloned().collect();
    counts.sort();

    let mut hand_count = counts;

    let l = hand_count.len();
    if l == 0 {
        hand_count = vec![jokers];
    } else {
        hand_count[l - 1] += jokers;
    }

    if hand_count == vec![1, 1, 1, 1, 1] {
        // high card
        return 1;
    }
    if hand_count == vec![1, 1, 1, 2] {
        // one pair
        return 2;
    }
    if hand_count == vec![1, 2, 2] {
        // two pair
        return 3;
    }
    if hand_count == vec![1, 1, 3] {
        // three of a kind
        return 4;
    }
    if hand_count == vec![2, 3] {
        // full house
        return 5;
    }
    if hand_count == vec![1, 4] {
        // four of a kind
        return 6;
    }
    if hand_count == vec![5] {
        // five of a kind
        return 7;
    }
    0
}

fn parse_line(line: &str) -> (&str, u32) {
    let parts: Vec<_> = line.split(" ").collect();
    (parts[0], parts[1].parse::<u32>().unwrap())
}

fn main() {
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("couldn't read input file");

    // part1(&input);
    part2(&input);
}
