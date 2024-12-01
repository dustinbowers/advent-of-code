use std::collections::HashMap;

fn parse_input(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .collect::<Vec<&str>>()
        .iter()
        .map(|s| s.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>()
}
// fn print_field(field: &Vec<Vec<char>>) {
//     field.iter().all(|line| {
//         println!("{}", line.iter().collect::<String>());
//         return true;
//     });
//     println!();
// }
fn calculate_weight(field: &Vec<Vec<char>>) -> usize {
    field.iter().rev().enumerate().fold(0, |acc, (r, line)| {
        line.iter().filter(|c| **c == 'O').count() * (r + 1) + acc
    })
}

fn transpose2<T>(v: Vec<Vec<T>>) -> Vec<Vec<T>> {
    assert!(!v.is_empty());
    let len = v[0].len();
    let mut iters: Vec<_> = v.into_iter().map(|n| n.into_iter()).collect();
    (0..len)
        .map(|_| {
            iters
                .iter_mut()
                .map(|n| n.next().unwrap())
                .collect::<Vec<T>>()
        })
        .collect()
}
fn flip_cols(field: &mut Vec<Vec<char>>) {
    field.iter_mut().for_each(|row| row.reverse())
}
fn flip_rows(field: &mut Vec<Vec<char>>) {
    field.reverse()
}
fn run_cycle(field: Vec<Vec<char>>) -> Vec<Vec<char>> {
    // roll north
    let mut field = transpose2(field);
    field = roll_field_left(&field);

    // roll west
    field = transpose2(field);
    field = roll_field_left(&field);

    // roll south
    flip_rows(&mut field);
    field = transpose2(field);
    field = roll_field_left(&field);

    // roll east
    flip_rows(&mut field);
    field = transpose2(field);
    field = roll_field_left(&field);

    // fix orientation
    flip_rows(&mut field);
    flip_cols(&mut field);

    field
}
fn roll_field_left(field: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let mut rolled_field: Vec<Vec<char>> = vec![];
    for line in field {
        rolled_field.push(roll_left(&line));
    }
    rolled_field
}
fn roll_left(line: &Vec<char>) -> Vec<char> {
    let mut inds = line
        .iter()
        .enumerate()
        .filter_map(|(i, c)| if *c == '#' { Some(i) } else { None })
        .collect::<Vec<_>>();
    inds.push(line.len());

    let mut last_ind = 0usize;
    let mut out: Vec<char> = vec![];
    for ind in inds {
        // find O count up to ind
        let ct = &line[last_ind..ind].iter().fold(0, |acc, v| {
            if *v == 'O' {
                return acc + 1;
            }
            acc
        });
        let mut rocks = vec!['O'; *ct as usize];
        let mut spaces = vec!['.'; (ind - last_ind) - (*ct as usize)];
        out.append(&mut rocks);
        out.append(&mut spaces);
        if ind == line.len() {
            continue;
        }
        out.push('#');
        last_ind = ind + 1;
    }
    out
}
fn part1(input: &str) {
    let field = parse_input(&input);

    let field = transpose2(field);
    let mut rolled_field = roll_field_left(&field);
    rolled_field = transpose2(rolled_field);

    let total = calculate_weight(&rolled_field);
    println!("total weight = {}", total);
}
fn part2(input: &str) {
    let mut field = parse_input(&input);

    let mut history: HashMap<String, usize> = HashMap::new();
    let mut cycle_at = 0;
    for i in 0..300 {
        field = run_cycle(field);
        let field_str = field
            .iter()
            .map(|r| r.iter().collect::<String>())
            .collect::<Vec<String>>()
            .join("");
        if history.contains_key(&field_str) {
            if cycle_at == 0 {
                cycle_at = i;
                history.clear();
                history.insert(field_str, i);
                // println!("Found beginning of cycle at {}", i);
                continue;
            } else {
                // println!("Found end of cycle. Cycle size = {}", i - cycle_at);
                // found the cycle, so we can fast-forward through all of them
                let mut remaining = 1_000_000_000 - i - 1;
                remaining %= i - cycle_at;
                let mut field2 = field.clone();
                for _ in 0..remaining {
                    field2 = run_cycle(field2);
                }
                let weight = calculate_weight(&field2);
                println!("Total weight = {}", weight);
                return;
            }
        }
        history.insert(field_str, i);
    }
}
fn main() {
    // let input_filename = "input_example.txt";
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found.");

    part1(&input); // 106517
    part2(&input); // 79723
}

#[cfg(test)]
#[test]
fn test_transpose2() {
    let input = vec![vec!['a', 'b', 'c']];
    let expected = vec![vec!['a'], vec!['b'], vec!['c']];
    assert_eq!(expected, transpose2(input));
}

#[test]
fn test_calculate_weight() {
    let f = vec![vec!['O', '.', 'O'], vec!['O', '.', '.']];
    assert_eq!(5, calculate_weight(&f));
}

#[test]
fn test_flip_cols() {
    let mut input = vec![vec!['1', '2'], vec!['3', '4']];
    let expected = vec![vec!['2', '1'], vec!['4', '3']];
    flip_cols(&mut input);
    assert_eq!(expected, input);
}
