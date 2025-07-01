package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type point struct {
	x int
	y int
}

func readInput() ([][]int, []point) {
	input, _ := os.ReadFile("./input.test.txt")
	inputStr := string(input)
	inputLines := strings.Split(inputStr, "\n")

	result := [][]int{}

	startPoints := []point{}

	for r, row := range inputLines {

		line := []int{}
		for c, char := range strings.Split(row, "") {
			charInt, _ := strconv.Atoi(char)
			line = append(line, charInt)

			if charInt == 0 {
				startPoints = append(startPoints, point{c, r})
			}
		}

		result = append(result, line)

	}
	return result, startPoints
}

func getTrailCount(fields [][]int, targetSet *map[point]bool, x int, y int) {
	z := fields[y][x]

	if z == 9 {
		targetPoint := point{x, y}
		dereferencedTargetSet := *targetSet
		dereferencedTargetSet[targetPoint] = true
		return
	}

	fieldLen := len(fields[0])
	fieldHeight := len(fields)

	if x > 0 {
		// left
		targetZ := fields[y][x-1]
		if targetZ-z == 1 {
			getTrailCount(fields, targetSet, x-1, y)
		}
	}
	if x < fieldHeight-1 {
		// right
		targetZ := fields[y][x+1]
		if targetZ-z == 1 {
			getTrailCount(fields, targetSet, x+1, y)
		}
	}

	if y > 0 {
		// up
		targetZ := fields[y-1][x]
		if targetZ-z == 1 {
			getTrailCount(fields, targetSet, x, y-1)
		}
	}
	if y < fieldLen-1 {
		// down
		targetZ := fields[y+1][x]
		if targetZ-z == 1 {
			getTrailCount(fields, targetSet, x, y+1)
		}
	}
	return

}

func part1() {
	input, startPoints := readInput()

	sum := 0

	for _, origin := range startPoints {
		targetSet := make(map[point]bool)
		getTrailCount(input, &targetSet, origin.x, origin.y)

		sum += len(targetSet)
	}

	fmt.Println(sum)
}

func getTrailCount2(fields [][]int, x int, y int) int {
	z := fields[y][x]

	if z == 9 {
		return 1
	}

	fieldLen := len(fields[0])
	fieldHeight := len(fields)

	sum := 0

	if x > 0 {
		// left
		targetZ := fields[y][x-1]
		if targetZ-z == 1 {
			sum += getTrailCount2(fields, x-1, y)
		}
	}
	if x < fieldHeight-1 {
		// right
		targetZ := fields[y][x+1]
		if targetZ-z == 1 {
			sum += getTrailCount2(fields, x+1, y)
		}
	}

	if y > 0 {
		// up
		targetZ := fields[y-1][x]
		if targetZ-z == 1 {
			sum += getTrailCount2(fields, x, y-1)
		}
	}
	if y < fieldLen-1 {
		// down
		targetZ := fields[y+1][x]
		if targetZ-z == 1 {
			sum += getTrailCount2(fields, x, y+1)
		}
	}
	return sum

}

func part2() {
	input, startPoints := readInput()

	sum := 0

	for _, origin := range startPoints {

		sum += getTrailCount2(input, origin.x, origin.y)
	}

	fmt.Println(sum)
}

func main() {
	part1()
	part2()
}
