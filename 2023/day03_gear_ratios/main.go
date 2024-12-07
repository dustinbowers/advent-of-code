package main

import (
	"fmt"
	"strconv"
	"strings"
)
import "os"

type Gear struct {
	i int
	j int
}

func main() {
	fn := "input_test.txt"

	contents, err := os.ReadFile(fn)
	if err != nil {
		fmt.Println("Error: ", err)
		os.Exit(-1)
	}

	gears := make([]Gear, 0)
	numField := make([][]int, 0)
	numIdx := 1
	numsByIdx := make(map[int]int)

	lines := strings.Split(string(contents), "\n")
	cols := len(lines[0])
	rows := len(lines)
	currNumStr := ""
	for i := 0; i < rows; i++ {
		numFieldLine := make([]int, cols)
		for j := 0; j < cols; j++ {
			c := lines[i][j]

			// Find Gears
			fmt.Printf("%c", c)
			if c == '*' {
				gears = append(gears, Gear{i, j})
			}

			// number "key" field
			if c >= '0' && c <= '9' {
				numFieldLine[j] = numIdx
				currNumStr += string(c)
			} else {
				if currNumStr != "" {
					n, _ := strconv.Atoi(currNumStr)
					numsByIdx[numIdx] = n
					currNumStr = ""
				}
				numIdx++
			}
		}
		if currNumStr != "" {
			n, _ := strconv.Atoi(currNumStr)
			numsByIdx[numIdx] = n
			currNumStr = ""
		}
		numField = append(numField, numFieldLine)
		fmt.Println()
	}
	fmt.Printf("Gears = %v\n\n", gears)
	for i := range numField {
		fmt.Printf("Field = %v\n", numField[i])
	}

	fmt.Printf("numsByIdx = %v\n", numsByIdx)

	gearSum := 0
	for _, gear := range gears {
		gearNums := findSurroundingNumIdx(gear, numField)
		if len(gearNums) == 2 {
			n1 := numsByIdx[gearNums[0]]
			n2 := numsByIdx[gearNums[1]]
			gearSum += n1 * n2
			fmt.Printf("Adding gear product %v to current gearSum. n1 = %v, n2 = %v, new gearSum = %v\n", n1*n2, n1, n2, gearSum)
			if n1 == 0 || n2 == 0 {
				os.Exit(0)
			}
		}
	}
	fmt.Printf("\nPart 2 gear product sum: %d", gearSum) // 72553319
}

func findSurroundingNumIdx(g Gear, numField [][]int) []int {
	adjacentNumMap := make(map[int]struct{})
	rows := len(numField)
	cols := len(numField[0])
	// Iterate around the immediately adjacent cells of the gear
	for i := g.i - 1; i <= g.i+1; i++ {
		if i < 0 || i >= rows {
			continue
		}
		for j := g.j - 1; j <= g.j+1; j++ {
			if j < 0 || j >= cols {
				continue
			}
			if numField[i][j] > 0 {
				adjacentNumMap[numField[i][j]] = struct{}{}
			}
		}
	}

	if len(adjacentNumMap) == 2 {
		fmt.Printf("Checking gear %v\t", g)
		fmt.Printf("adjacentNumMap = %v\n", adjacentNumMap)
	}
	// extract keys of the set/map
	keys := make([]int, 0)
	for k := range adjacentNumMap {
		keys = append(keys, k)
	}
	return keys
}
