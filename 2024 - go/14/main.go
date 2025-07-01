package main

import (
	"fmt"
	"os"
	"regexp"
	"slices"
	"strconv"
	"strings"
)

type vec2 struct {
	x int
	y int
}

func mulVec2(vec vec2, m int) vec2 {
	return vec2{m * vec.x, m * vec.y}
}

func addVec2(a vec2, b vec2) vec2 {
	return vec2{a.x + b.x, a.y + b.y}
}

func wrapVec2(a vec2, b vec2) vec2 {
	return vec2{a.x % b.x, a.y % b.y}
}

type robot struct {
	id       int
	pos      vec2
	velocity vec2
}

func part1() {
	testSpace := vec2{101, 103}
	//space := vec2{101, 103}

	input, _ := os.ReadFile("input.txt")
	inputStr := string(input)
	lines := strings.Split(inputStr, "\n")

	r := regexp.MustCompile(`[\-\d]+`)

	robots := []robot{}

	for index, line := range lines {
		captures := r.FindAllString(line, -1)
		x, _ := strconv.Atoi(captures[0])
		y, _ := strconv.Atoi(captures[1])
		vx, _ := strconv.Atoi(captures[2])
		vy, _ := strconv.Atoi(captures[3])
		robot := robot{index, vec2{x, y}, vec2{vx, vy}}

		robots = append(robots, robot)
	}

	rounds := 100
	quadrant0 := 0
	quadrant1 := 0
	quadrant2 := 0
	quadrant3 := 0
	for _, robot := range robots {
		position := robot.pos
		vel := robot.velocity

		pos := addVec2(position, mulVec2(vel, rounds))
		wrappedPos := wrapVec2(pos, testSpace)
		if wrappedPos.x < 0 {
			wrappedPos.x += testSpace.x
		}
		if wrappedPos.y < 0 {
			wrappedPos.y += testSpace.y
		}

		if wrappedPos.x > testSpace.x/2 {
			if wrappedPos.y > testSpace.y/2 {
				quadrant0++
			}
			if wrappedPos.y < testSpace.y/2 {
				quadrant1++
			}
		}
		if wrappedPos.x < testSpace.x/2 {
			if wrappedPos.y > testSpace.y/2 {
				quadrant2++
			}
			if wrappedPos.y < testSpace.y/2 {
				quadrant3++
			}
		}

	}
	fmt.Println(quadrant0 * quadrant1 * quadrant2 * quadrant3)

}

func printMap(size vec2, positions []vec2) {
	lines := make([][]int, size.y)

	for y := range lines {
		lines[y] = slices.Repeat([]int{0}, size.x)
	}

	for _, pos := range positions {
		lines[pos.y][pos.x]++
	}

	for _, line := range lines {
		fmt.Println()
		for _, char := range line {
			if char == 0 {
				fmt.Print(" ")
				continue
			}
			fmt.Print(char)
		}
		fmt.Println()

	}
}

func part2() {
	testSpace := vec2{101, 103}
	//space := vec2{101, 103}

	input, _ := os.ReadFile("./input.txt")

	inputStr := string(input)
	lines := strings.Split(inputStr, "\n")

	r := regexp.MustCompile(`[\-\d]+`)

	robots := []robot{}

	for index, line := range lines {
		captures := r.FindAllString(line, -1)
		x, _ := strconv.Atoi(captures[0])
		y, _ := strconv.Atoi(captures[1])
		vx, _ := strconv.Atoi(captures[2])
		vy, _ := strconv.Atoi(captures[3])
		robot := robot{index, vec2{x, y}, vec2{vx, vy}}

		robots = append(robots, robot)
	}

	max_rounds := testSpace.x * testSpace.y

	for round := 0; round < max_rounds; round++ {
		positions := []vec2{}
		posMap := make(map[vec2]bool)
		for _, robot := range robots {
			position := robot.pos
			vel := robot.velocity

			pos := addVec2(position, mulVec2(vel, round))
			wrappedPos := wrapVec2(pos, testSpace)
			if wrappedPos.x < 0 {
				wrappedPos.x += testSpace.x
			}
			if wrappedPos.y < 0 {
				wrappedPos.y += testSpace.y
			}
			positions = append(positions, wrappedPos)
			posMap[wrappedPos] = true
		}

		if len(positions) == len(posMap) {
			fmt.Println("Round", round)
			printMap(testSpace, positions)

		}

	}

}

func main() {
	part1()
	part2()
}
