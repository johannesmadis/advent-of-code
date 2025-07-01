package main

import (
	"fmt"
	"os"
	"strings"
)

type vec2 struct {
	x int
	y int
}

func getCurrent(openSet map[vec2]int) vec2 {
	minimum := 999999
	minVec := vec2{}

	for item, dist := range openSet {
		if dist < minimum {
			minimum = dist
			minVec = item
		}
	}

	return minVec
}

func getNeighbors(origin vec2) []vec2 {
	neighbors := []vec2{}

	neighbors = append(neighbors, vec2{origin.x - 1, origin.y})

	neighbors = append(neighbors, vec2{origin.x + 1, origin.y})

	neighbors = append(neighbors, vec2{origin.x, origin.y - 1})

	neighbors = append(neighbors, vec2{origin.x, origin.y + 1})

	return neighbors
}
func getHistory(parents map[vec2]vec2, target vec2) []vec2 {
	history := []vec2{}

	currentNode := target
	for true {
		parent, exists := parents[currentNode]
		if exists {
			history = append(history, parent)
			currentNode = parent
		} else {
			break
		}

	}
	return history
}

func dijkstra(fields [][]string, start vec2) (map[vec2]int, map[vec2]vec2) {

	w := len(fields[0])
	h := len(fields)

	distances := make(map[vec2]int)

	for y, line := range fields {
		for x := range line {
			distances[vec2{x, y}] = w * h
		}
	}

	parents := make(map[vec2]vec2)
	parents[start] = vec2{start.x - 1, start.y}
	closedSet := make(map[vec2]bool)
	openSet := make(map[vec2]int)
	openSet[start] = 0
	distances[start] = 0

	for len(openSet) > 0 {
		current := getCurrent(openSet)

		neighbors := getNeighbors(current)
		delete(openSet, current)

		closedSet[current] = true
		for _, neighbor := range neighbors {
			if fields[neighbor.y][neighbor.x] != "#" && !closedSet[neighbor] {
				_, exists := openSet[neighbor]
				bonusDistance := 0
				if (neighbor.y-current.y != current.y-parents[current].y) || (neighbor.x-current.x != current.x-parents[current].x) {
					bonusDistance = 1000
				}

				altDist := distances[current] + 1 + bonusDistance

				if exists {
					if openSet[neighbor] > altDist {
						openSet[neighbor] = altDist
						parents[neighbor] = current
						distances[neighbor] = altDist
					}
				} else {
					openSet[neighbor] = altDist
					parents[neighbor] = current
					distances[neighbor] = altDist
				}
			}
		}

	}

	delete(parents, start)

	return distances, parents

}

func part1() {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)
	inputLines := strings.Split(inputStr, "\n")

	fields := [][]string{}
	var start vec2
	var end vec2

	for y, line := range inputLines {
		currentLine := []string{}
		for x, char := range strings.Split(line, "") {
			currentLine = append(currentLine, char)
			if char == "S" {
				start = vec2{x, y}

			}
			if char == "E" {
				end = vec2{x, y}

			}
		}
		fields = append(fields, currentLine)
	}

	distances, parents := dijkstra(fields, start)

	history := getHistory(parents, end)

	for i, item := range history {
		char := "O"
		if i > 0 && distances[history[i-1]]-distances[item] != 1 {
			char = "X"
		}
		fields[item.y][item.x] = char
	}

	for _, line := range fields {
		fmt.Println(strings.Join(line, ""))
	}

	fmt.Println(distances[end], len(history))

}

func main() {
	part1()
}
