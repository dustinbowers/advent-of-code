use std::collections::HashSet;

fn parse_input(input: &str) -> Vec<Vec<char>> {
    input
        .lines()
        .collect::<Vec<&str>>()
        .iter()
        .map(|s| s.chars().collect::<Vec<char>>())
        .collect::<Vec<Vec<char>>>()
}

fn find_galaxies(cosmos: &Vec<Vec<char>>) -> Vec<(i64, i64)> {
    cosmos
        .iter()
        .enumerate()
        .map(|(i, r)| {
            r.iter()
                .enumerate()
                .filter_map(move |(j, c)| {
                    if *c == '#' {
                        return Some((i as i64, j as i64));
                    }
                    None
                })
                .collect::<Vec<_>>()
        })
        .flatten()
        .collect::<Vec<_>>()
}

fn expand_cosmos(
    galaxies: &Vec<(i64, i64)>,
    cols: usize,
    rows: usize,
    expansion_size: i64,
) -> (Vec<i64>, Vec<i64>) {
    let mut galaxy_i: HashSet<i64> = HashSet::new();
    let mut galaxy_j: HashSet<i64> = HashSet::new();
    for g in galaxies {
        galaxy_i.insert(g.0);
        galaxy_j.insert(g.1);
    }

    let mut row_expansion = vec![0; rows];
    let mut col_expansion = vec![0; cols];
    let mut row_exp = 0;
    let mut col_exp = 0;
    for i in 0..rows {
        if !galaxy_i.contains(&(i as i64)) {
            row_exp += expansion_size;
        }
        row_expansion[i] = row_exp;
    }
    for j in 0..cols {
        if !galaxy_j.contains(&(j as i64)) {
            col_exp += expansion_size;
        }
        col_expansion[j] = col_exp;
    }
    println!(
        "row_expansion = {:?}\ncol_expansion = {:?}\ngalaxy_i = {:?}\ngalaxy_j = {:?}",
        row_expansion, col_expansion, galaxy_i, galaxy_j
    );
    (row_expansion, col_expansion)
}

fn expand_galaxies(
    galaxies: &Vec<(i64, i64)>,
    row_exp: &Vec<i64>,
    col_exp: &Vec<i64>,
) -> Vec<(i64, i64)> {
    galaxies
        .iter()
        .map(|g| (g.0 + row_exp[g.0 as usize], g.1 + col_exp[g.1 as usize]))
        .collect()
}

fn dist(a: &(i64, i64), b: &(i64, i64)) -> i64 {
    (a.0 - b.0).abs() + (a.1 - b.1).abs()
}

fn part1(input: &str) {
    let cosmos = parse_input(&input);
    let rows = cosmos.len();
    let cols = cosmos[0].len();
    let galaxies = find_galaxies(&cosmos);
    println!("Galaxies = {:?}", galaxies);
    let (row_exp, col_exp) = expand_cosmos(&galaxies, rows, cols, 1);
    let expanded_galaxies = expand_galaxies(&galaxies, &row_exp, &col_exp);
    println!(
        "Rows = {}, Cols = {}\nCosmos = {:?}\nGalaxies = {:?}",
        rows, cols, cosmos, expanded_galaxies
    );

    let mut total = 0;
    let mut total_pairs = 0;
    let l = expanded_galaxies.len();
    for (i, _) in expanded_galaxies.iter().enumerate() {
        for j in i + 1..l {
            let d = dist(&expanded_galaxies[i], &expanded_galaxies[j]);
            // println!("calculating distance between {} and {} = {}", i, j, d);
            total += d;
            total_pairs += 1;
        }
    }
    println!("Total pairs = {}", total_pairs);
    println!("Total distance between all galaxies = {}", total);
}

fn part2(input: &str) {
    let cosmos = parse_input(&input);
    let rows = cosmos.len();
    let cols = cosmos[0].len();
    let galaxies = find_galaxies(&cosmos);
    println!("Galaxies = {:?}", galaxies);
    let (row_exp, col_exp) = expand_cosmos(&galaxies, rows, cols, 999999);
    let expanded_galaxies = expand_galaxies(&galaxies, &row_exp, &col_exp);
    println!(
        "Rows = {}, Cols = {}\nCosmos = {:?}\nGalaxies = {:?}",
        rows, cols, cosmos, expanded_galaxies
    );

    let mut total = 0;
    let mut total_pairs = 0;
    let l = expanded_galaxies.len();
    for (i, _) in expanded_galaxies.iter().enumerate() {
        for j in i + 1..l {
            let d = dist(&expanded_galaxies[i], &expanded_galaxies[j]);
            total += d;
            total_pairs += 1;
        }
    }
    println!("Total pairs = {}", total_pairs);
    println!("Total distance between all galaxies = {}", total);
}

fn main() {
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found.");

    part1(&input);
    part2(&input);
}
