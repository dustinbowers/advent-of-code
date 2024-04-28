
fn part1(input : &str) {

}

fn main() {
    let input_filename = "input_example.txt";
    let input = std::fs::read_to_string(input_filename).expect("File not found.");

    part1(&input);
}
