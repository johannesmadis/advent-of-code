package main

import (
	"fmt"
	"os"
	"strings"
)

type point struct {
	x int
	y int
}

func addPoint(a point, b point) point {
	return point{a.x + b.x, a.y + b.y}
}
func deltaPoint(a point, b point) point {
	return point{b.x - a.x, b.y - a.y}
}

func mulPoint(a point, i int) point {
	return point{a.x * i, a.y * i}
}

func readInput() (map[string][]point, int, int) {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	lines := strings.Split(inputStr, "\n")

	antennae := make(map[string][]point)

	for y, line := range lines {
		for x, col := range strings.Split(line, "") {
			if col == "." {
				continue
			}

			list, exists := antennae[col]
			if !exists {
				list = []point{}
				antennae[col] = list
			}

			c := point{x, y}

			antennae[col] = append(list, c)

		}
	}
	return antennae, len(lines[0]), len(lines)
}

func part1() {
	antennae, width, height := readInput()

	antinodes := make(map[point]bool)

	for _, frequency := range antennae {
		for _, a := range frequency {
			for _, b := range frequency {
				if a == b {
					continue
				}
				delta := deltaPoint(a, b)
				// add to b to get as far from a as a is from b
				// reverese not necessary because this happens in loop where b is a
				antinode := addPoint(b, delta)

				if antinode.x >= 0 && antinode.x < width && antinode.y >= 0 && antinode.y < height {
					antinodes[antinode] = true
				}

			}
		}
	}

	fmt.Println("Part1: ", len(antinodes))

}

func part2() {
	antennae, width, height := readInput()

	antinodes := make(map[point]bool)

	for _, frequency := range antennae {
		for _, a := range frequency {
			for _, b := range frequency {
				if a == b {
					continue
				}
				delta := deltaPoint(a, b)
				// keep adding deltas to a until out of bounds
				// no need to do reverse since this will happen when b is a

				temp_base := a
				for true {
					antinode := addPoint(temp_base, delta)

					if antinode.x < 0 || antinode.x >= width || antinode.y < 0 || antinode.y >= height {
						break
					}

					antinodes[antinode] = true
					temp_base = antinode

				}

			}
		}
	}

	fmt.Println("Part2: ", len(antinodes))
}

func main() {
	part1()

	part2()
}
