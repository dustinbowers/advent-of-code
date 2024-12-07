use std::fs;

fn part1(input: String) {
    let mut seeds: Vec<usize> = vec![];

    let mut seed_to_soil: Vec<(usize, usize, usize)> = vec![];
    let mut soil_to_fertilizer: Vec<(usize, usize, usize)> = vec![];
    let mut fertilizer_to_water: Vec<(usize, usize, usize)> = vec![];
    let mut water_to_light: Vec<(usize, usize, usize)> = vec![];
    let mut light_to_temperature: Vec<(usize, usize, usize)> = vec![];
    let mut temperature_to_humidity: Vec<(usize, usize, usize)> = vec![];
    let mut humidity_to_location: Vec<(usize, usize, usize)> = vec![];

    let mut line_heading = "Seeds:";
    for (i, l) in input.lines().into_iter().enumerate() {
        if i == 0 {
            seeds = parse_line_to_vec(l);
        }
        let mut nums = vec![];
        match l {
            "" | "\n" | "\r\n" => {}
            "seed-to-soil map:"
            | "soil-to-fertilizer map:"
            | "fertilizer-to-water map:"
            | "water-to-light map:"
            | "light-to-temperature map:"
            | "temperature-to-humidity map:"
            | "humidity-to-location map:" => {
                line_heading = l;
            }
            _ => {
                nums = parse_line_to_vec(l);
            }
        }
        if nums.len() == 0 {
            continue;
        }
        println!("({}) - {:?}", line_heading, nums);

        // parse the map ranges
        match line_heading {
            "seed-to-soil map:" => {
                seed_to_soil.push((nums[0], nums[1], nums[2]));
            }
            "soil-to-fertilizer map:" => {
                soil_to_fertilizer.push((nums[0], nums[1], nums[2]));
            }
            "fertilizer-to-water map:" => {
                fertilizer_to_water.push((nums[0], nums[1], nums[2]));
            }
            "water-to-light map:" => {
                water_to_light.push((nums[0], nums[1], nums[2]));
            }
            "light-to-temperature map:" => {
                light_to_temperature.push((nums[0], nums[1], nums[2]));
            }
            "temperature-to-humidity map:" => {
                temperature_to_humidity.push((nums[0], nums[1], nums[2]));
            }
            "humidity-to-location map:" => {
                humidity_to_location.push((nums[0], nums[1], nums[2]));
            }
            _ => {}
        }
    }

    // Part 1
    ///////////////////////////////////////
    // let mut locations : Vec<usize> = vec![];
    // for seed in seeds {
    //     let soil = determine_mapping(&seed_to_soil, seed);
    //     let fertilizer = determine_mapping(&soil_to_fertilizer, soil);
    //     let water = determine_mapping(&fertilizer_to_water, fertilizer);
    //     let light = determine_mapping(&water_to_light, water);
    //     let temperature = determine_mapping(&light_to_temperature, light);
    //     let humidity = determine_mapping(&temperature_to_humidity, temperature);
    //     let location = determine_mapping(&humidity_to_location, humidity);
    //
    //     println!("Seed {} => Soil {} => Fertilizer {} => Water {} => Light {} => Temp {} => Humidity {} => Location {}", seed, soil, fertilizer, water, light, temperature, humidity, location);
    //
    //     locations.push(location);
    // }
    // dbg!(&locations);
    // let lowest_location = locations.iter().min().unwrap();
    // println!("Part 1, lowest-location ID: {}", lowest_location);
    ////////////////////////
    //

    //
    // NAIVE Part 2
    let mut lowest_location = usize::MAX;
    let len = seeds.len()/2;
    for i in 1..len {
        let start = seeds[i-1];
        let range = seeds[i];
        println!("i={} of {}: start = {}, range = {}", i, len, start, range);
        for j in start..=start+range {
            let soil = determine_mapping(&seed_to_soil, j);
            let fertilizer = determine_mapping(&soil_to_fertilizer, soil);
            let water = determine_mapping(&fertilizer_to_water, fertilizer);
            let light = determine_mapping(&water_to_light, water);
            let temperature = determine_mapping(&light_to_temperature, light);
            let humidity = determine_mapping(&temperature_to_humidity, temperature);
            let location = determine_mapping(&humidity_to_location, humidity);

            if location < lowest_location {
                lowest_location = location;
                println!("Lowest location = {}", lowest_location);
            }
        }
    }

}

fn determine_mapping(map : &Vec<(usize, usize, usize)>, source : usize) -> usize {
    // Find a destination range if one exists
    for ranges in map {
        let (d, s, r)  = ranges;
        if source >= *s && source <= *s + *r {
            return *d + source - *s;
        }
    }
    source
}

fn parse_line_to_vec(line: &str) -> Vec<usize> {
    return line
        .chars()
        .filter(|c| c.is_digit(10) || c == &' ')
        .collect::<String>()
        .split_whitespace()
        .map(|s| s.parse::<usize>().unwrap())
        .collect();
}

fn main() {
    let input = fs::read_to_string("input_test.txt").expect("couldn't read input file");
    part1(input);
}
