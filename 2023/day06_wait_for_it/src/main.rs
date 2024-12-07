use std::fs;

fn part1(input : &str) {

    let (times, dists) = parse_lines(input);

    println!("Times = {:?}\nDistances = {:?}", times, dists);
    let mut win_product : usize = 1;
    for (i, t) in times.iter().enumerate() {
        let mut wins : usize = 0;
        let target_dist = dists[i];
        for hold in 1..*t {
            let total_dist = calc_distance(hold, *t);
            if total_dist >= target_dist {
                wins += 1;
                // println!("Total time {}ms, holding for {}ms travels {}mm", *t, hold, total_dist);

            }
        }
        win_product *= wins;
    }
    println!("\nPart 1, win product = {}\n", win_product);
}

fn part2(input : &str) {

    let (time, dist) = parse_lines_into_numbers(input);
    println!("time = {}, dist = {}", time, dist);

    // explore left half
    let mut left = 0usize;
    let mut right = time / 2;
    while right - 1 != left {
        let mid = left + (right - left) / 2;
        if calc_distance(mid, time) < dist {
            left = mid;
        } else {
            right = mid;
        }
    }
    let left_bound = right;

    // explore right half
    let mut left = time / 2;
    let mut right = time;
    while right - 1 != left {
        let mid = left + (right - left) / 2;
        if calc_distance(mid, time) >= dist {
            left = mid;
        } else {
            right = mid;
        }
    }
    let right_bound = left;

    if calc_distance(left_bound, time) >= dist {
        println!("left_bound of {} wins!", left_bound);
    }
    if calc_distance(right_bound, time) >= dist {
        println!("right_bound of {} wins!", right_bound);
    }

    println!("\nPart 2, possible solutions: {}\n", right_bound - left_bound + 1);
}

fn calc_distance(hold_ms : usize, time : usize) -> usize {
    let travel_time = time - hold_ms;
    let total_dist = travel_time * hold_ms;
    total_dist
}

fn parse_lines(input : &str) -> (Vec<usize>, Vec<usize>) {
    let lines = input.lines().collect::<Vec<&str>>();
    let times = lines[0]
        .chars()
        .filter(|c| c.is_digit(10) || c == &' ')
        .collect::<String>()
        .split_whitespace()
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
    let distances = lines[1]
        .chars()
        .filter(|c| c.is_digit(10) || c == &' ')
        .collect::<String>()
        .split_whitespace()
        .map(|s| s.parse::<usize>().unwrap())
        .collect();

    (times, distances)
}

fn parse_lines_into_numbers(input : &str) -> (usize, usize) {
    let lines = input.lines().collect::<Vec<&str>>();
    let times = lines[0]
        .chars()
        .filter(|c| c.is_digit(10))
        .collect::<String>()
        .parse::<usize>()
        .unwrap();
    let distances = lines[1]
        .chars()
        .filter(|c| c.is_digit(10))
        .collect::<String>()
        .parse::<usize>()
        .unwrap();

    (times, distances)
}

fn main() {
    let input = fs::read_to_string("input_test.txt").expect("couldn't read input file");
    part1(&input);
    part2(&input);
}
