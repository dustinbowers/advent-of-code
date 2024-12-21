fn parse_input(input: &str) -> Vec<Vec<Vec<i32>>> {
    let fields_str = input.split("\n\n").collect::<Vec<&str>>();
    let mut fields: Vec<Vec<Vec<i32>>> = vec![];

    for f_str in fields_str {
        let mut new_field: Vec<Vec<i32>> = vec![];
        for l in f_str.lines() {
            let mut num_vec: Vec<i32> = vec![];
            for c in l.chars() {
                match c {
                    '#' => num_vec.push(1),
                    '.' => num_vec.push(0),
                    _ => {}
                }
            }
            new_field.push(num_vec);
        }
        fields.push(new_field);
    }
    fields
}

fn print_field(field: &Vec<Vec<i32>>) {
    for r in field {
        for c in r {
            print!("{} ", c)
        }
        println!();
    }
}

fn find_symmetry(field: &Vec<Vec<i32>>, smudges: bool) -> Option<usize> {
    // println!("Finding symmetry of:");
    // print_field(&field);

    let rows = field.len();
    if rows == 0 {
        panic!("not enough rows!");
    }
    let symmetry_ind;
    for s_ind in 0..rows - 1 {
        let l_size = s_ind;
        let r_size = rows - s_ind - 2;
        let n = l_size.min(r_size);
        let mut total_diff = 0;
        // println!("------------ n = {}", n);
        for i in 0..=n {
            let left = &field[s_ind - i];
            let right = &field[s_ind + i + 1];
            // println!("(s_ind = {}, L = {}, R = {}) comparing left vs right:\nL = {:?}\nR = {:?}", s_ind, s_ind - i, s_ind + i + 1, left, right);
            total_diff += compare_diff(left, right);
        }
        if !smudges && total_diff == 0 {
            // println!("FOUND SYMMETRY AT {}", s_ind);
            symmetry_ind = s_ind;
            return Some(symmetry_ind);
        } else if smudges && total_diff == 1 {
            // println!("FOUND SMUDGED SYMMETRY AT {}", s_ind);
            symmetry_ind = s_ind;
            return Some(symmetry_ind);
        }
    }
    None
}

fn compare_diff(a: &Vec<i32>, b: &Vec<i32>) -> i32 {
    let mut diff = 0;
    for (i, _) in a.iter().enumerate() {
        if a[i] != b[i] {
            diff += 1;
        }
    }
    diff
}
fn transpose(matrix: Vec<Vec<i32>>) -> Vec<Vec<i32>> {
    let num_cols = matrix.first().unwrap().len();
    let mut row_iters: Vec<_> = matrix.into_iter().map(Vec::into_iter).collect();
    let mut out: Vec<Vec<_>> = (0..num_cols).map(|_| Vec::new()).collect();

    for out_row in out.iter_mut() {
        for it in row_iters.iter_mut() {
            out_row.push(it.next().unwrap());
        }
    }
    out
}
fn solve(input: &str, smudges: bool) -> usize {
    let fields = parse_input(input);
    let mut total = 0;
    for (_, f) in fields.iter().enumerate() {
        // println!("field #{}", i);
        let r_symmetry = find_symmetry(&f, smudges);
        match r_symmetry {
            Some(s) => {
                // println!("row symmetry at {}", s);
                total += (s + 1) * 100;
                continue;
            }
            None => {}
        };
        let t = transpose(f.to_vec());
        let c_symmetry = find_symmetry(&t, smudges);
        match c_symmetry {
            Some(s) => {
                // println!("col symmetry at {}", s);
                total += s + 1;
                continue;
            }
            None => {}
        };
    }
    // println!("Total = {}", total);
    total
}

fn part1(input: &str) {
    let t = solve(input, false);
    println!("Part 1 total = {}", t);
}

fn part2(input: &str) {
    let t = solve(input, true);
    println!("Part 2 total = {}", t);
}

fn main() {
    // let input_filename = "input_example.txt";
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).expect("File error");

    part1(&input);
    part2(&input);
}
