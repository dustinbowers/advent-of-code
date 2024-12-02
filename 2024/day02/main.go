package main

import (
	"bufio"
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
)

func readInput(filename string) ([][]int, error) {
	file, err := os.Open(filename)
	if err != nil {
		return nil, err
	}

	var reports [][]int
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		parts := strings.Fields(scanner.Text())
		values := make([]int, len(parts))
		for i, p := range parts {
			v, err := strconv.ParseInt(p, 10, 64)
			if err != nil {
				return nil, err
			}
			values[i] = int(v)
		}
		reports = append(reports, values)
	}
	return reports, nil
}

func isSafe(report []int) bool {
	deltas := make([]int, len(report)-1)
	for i := 1; i < len(report); i++ {
		deltas[i-1] = report[i] - report[i-1]
	}
	c := 1
	if deltas[0] < 0 {
		c = -1
	}
	for _, d := range deltas {
		d2 := c * d
		if d2 < 1 || d2 > 3 {
			return false
		}
	}
	return true
}

func solve(reports [][]int) (int, int) {
	safeCt := 0
	safeCtWithDampener := 0
	for _, report := range reports {
		if isSafe(report) {
			safeCt += 1
		} else {
			for i := 0; i < len(report); i++ {
				dampenedReport := make([]int, 0)
				dampenedReport = append(dampenedReport, report[:i]...)
				dampenedReport = append(dampenedReport, report[i+1:]...)
				if isSafe(dampenedReport) {
					safeCtWithDampener += 1
					break
				}
			}
		}
	}
	return safeCt, safeCt + safeCtWithDampener
}

func main() {
	filename := "input.txt"
	if len(os.Args) == 2 {
		filename = os.Args[1]
	}
	if len(os.Args) > 2 {
		log.Fatalf("%s: <filename>", os.Args[0])
	}

	reports, err := readInput(filename)
	if err != nil {
		log.Fatal("Error:", err)
	}

	safeCt, safeCtWithDampener := solve(reports)
	fmt.Printf("Part1: safe_ct = %d\n", safeCt)
	fmt.Printf("Part2: safe_ct_with_dampener = %d\n", safeCtWithDampener)
}
