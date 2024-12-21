use std::fs;

fn parse_digits(t_num: &str) -> String {
    t_num
        .chars()
        .filter_map(|a| a.to_digit(10))
        .collect::<Vec<_>>()
        .iter()
        .map(ToString::to_string)
        .collect()
}

fn main() {
    let input = fs::read_to_string("input.txt").expect("couldn't read input file");
    let lines: Vec<String> = input.lines().map(String::from).collect();

    let mut total = 0;
    for l in lines {
        let parts: Vec<&str> = l.split(":").collect();
        let game_str = parts[0].to_owned();
        let marble_str = parts[1].trim();
        let game_num = parse_digits(&game_str).parse::<u32>().unwrap();
        println!("game_num = {}\nmarble_str = {}", game_num, marble_str);

        let games: Vec<&str> = marble_str.split("; ").collect();
        let mut max_red: u32 = 0;
        let mut max_green: u32 = 0;
        let mut max_blue: u32 = 0;
        for g in games {
            let parts: Vec<&str> = g.split(", ").collect();
            for p in parts {
                let pieces: Vec<&str> = p.split(" ").collect();
                let marble_ct = pieces[0].parse::<u32>().unwrap();
                let marble_color = pieces[1];

                match marble_color {
                    "red" => {
                        if marble_ct >= max_red {
                            max_red = marble_ct;
                        }
                    }
                    "green" => {
                        if marble_ct >= max_green {
                            max_green = marble_ct;
                        }
                    }
                    "blue" => {
                        if marble_ct >= max_blue {
                            max_blue = marble_ct;
                        }
                    }
                    _ => {}
                };
            }
        }
        total += max_red * max_green * max_blue;
    }

    println!("Total = {}", total);
}
