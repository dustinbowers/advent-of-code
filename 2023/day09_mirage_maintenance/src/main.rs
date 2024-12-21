fn extrapolate_right(nums: Vec<i32>) -> i32 {
    let mut diffs: Vec<Vec<i32>> = vec![];

    let mut new_line: Vec<i32> = nums.clone();
    diffs.push(nums);
    println!("new_line = {:?}", new_line);
    let all_zeros = false;
    while !all_zeros {
        new_line = calc_diffs(&new_line);
        diffs.push(new_line.clone());
        println!("diffs = {:?}", new_line);
        if check_all_zeros(&new_line) {
            break;
        }
    }
    for i in (0..diffs.len() - 1).rev() {
        let row_last = diffs[i].last().unwrap();
        let diff = diffs[i + 1].last().unwrap();
        let extrapolated_val = row_last + diff;
        diffs[i].push(extrapolated_val);
        println!("Extrapolated value = {}", extrapolated_val);
    }
    *diffs[0].last().unwrap()
}

fn check_all_zeros(nums: &Vec<i32>) -> bool {
    for i in nums {
        if *i != 0 {
            return false;
        }
    }
    true
}

fn calc_diffs(nums: &Vec<i32>) -> Vec<i32> {
    let mut output: Vec<i32> = vec![];
    for win in nums.windows(2) {
        output.push(win[1] - win[0]);
    }
    output
}

fn part1(input: &str) {
    let mut total = 0;
    for line in input.lines() {
        let nums = line
            .split_whitespace()
            .collect::<Vec<&str>>()
            .into_iter()
            .map(|n| n.parse::<i32>().unwrap())
            .collect::<Vec<i32>>();
        println!("\n\nnums = {:?}", nums);
        let n = extrapolate_right(nums);
        println!("extrapolated value = {}", n);
        total += n;
    }
    println!("Sum of extrapolated values = {}", total);
}

fn part2(input: &str) {
    let mut total = 0;
    for line in input.lines() {
        let mut nums = line
            .split_whitespace()
            .collect::<Vec<&str>>()
            .into_iter()
            .map(|n| n.parse::<i32>().unwrap())
            .collect::<Vec<i32>>();
        nums.reverse();
        println!("\n\nnums = {:?}", nums);
        let n = extrapolate_right(nums);
        println!("extrapolated value = {}", n);
        total += n;
    }
    println!("Sum of extrapolated values = {}", total);
}

fn main() {
    let input_filename = "input_test.txt";
    let input = std::fs::read_to_string(input_filename).unwrap();

    part1(&input);
    part2(&input);
}
