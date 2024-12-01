package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"os"
	"slices"
	"strconv"
	"strings"
)

func readInput(filename string) ([]int, []int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, nil, err
	}

	var left, right []int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		line := scanner.Text()
		parts := strings.Fields(line)
		if len(parts) != 2 {
			return nil, nil, fmt.Errorf("expected 2 parts, got %d", len(parts))
		}

		leftInt, err1 := strconv.ParseInt(parts[0], 10, 32)
		rightInt, err2 := strconv.ParseInt(parts[1], 10, 32)
		if err1 != nil || err2 != nil {
			return nil, nil, fmt.Errorf("invalid line: %s", line)
		}

		left = append(left, int(leftInt))
		right = append(right, int(rightInt))
	}
	return left, right, nil
}

func part1(left []int, right []int) int {
	sortDistance := 0
	for i := 0; i < len(left); i++ {
		sortDistance += int(math.Abs(float64(right[i] - left[i])))
	}
	return sortDistance
}

func part2(left []int, right []int) int {
	similarityScore := 0
	rightCts := make(map[int]int)
	for _, r := range right {
		rightCts[r] += 1
	}
	for _, l := range left {
		similarityScore += l * rightCts[l]
	}
	return similarityScore
}

func main() {
	filename := "input.txt"
	if len(os.Args) == 2 {
		filename = os.Args[0]
	}
	if len(os.Args) > 2 {
		log.Fatalf("%s: <filename>", os.Args[0])
	}

	left, right, err := readInput(filename)
	if err != nil {
		log.Fatal("Error:", err)
	}

	slices.Sort(left)
	slices.Sort(right)

	sortDistance := part1(left, right)
	fmt.Printf("Part1: sort_distance = %d\n", sortDistance)

	similarityScore := part2(left, right)
	fmt.Printf("Part2: similarity_score = %d\n", similarityScore)
}
