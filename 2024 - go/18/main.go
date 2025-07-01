package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

type vec2 struct {
	x int
	y int
}

func readMap(width int, height int, rounds int) [][]string {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	fields := [][]string{}
	for y := 0; y < height; y++ {
		line := []string{}
		for x := 0; x < width; x++ {
			line = append(line, ".")
		}
		fields = append(fields, line)
	}

	lines := strings.Split(inputStr, "\n")
	for i, line := range lines {
		if i >= rounds {
			break
		}
		values := strings.Split(line, ",")
		vX, _ := strconv.Atoi(values[0])
		vY, _ := strconv.Atoi(values[1])
		fields[vY][vX] = "#"

		if i == rounds-1 {
			fmt.Println("ANSWER", vX, vY)
		}

	}

	return fields
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

func getNeighbors2(fields [][]string, origin vec2) []vec2 {
	neighbors := []vec2{}
	w := len(fields[0])
	h := len(fields)

	if origin.x > 0 {
		neighbors = append(neighbors, vec2{origin.x - 1, origin.y})
	}
	if origin.x < w-1 {
		neighbors = append(neighbors, vec2{origin.x + 1, origin.y})
	}
	if origin.y > 0 {
		neighbors = append(neighbors, vec2{origin.x, origin.y - 1})
	}
	if origin.y < h-1 {
		neighbors = append(neighbors, vec2{origin.x, origin.y + 1})
	}

	return neighbors
}

func dijkstra2(fields [][]string, start vec2) (map[vec2]int, map[vec2]vec2) {
	/*
			for each vertex v in Graph.Vertices:
		           dist[v] ← INFINITY
		 5         prev[v] ← UNDEFINED
		           add v to Q
		       dist[source] ← 0

		      while Q is not empty:          u ← vertex in Q with minimum dist[u]
		         remove u from Q

		          for each neighbor v of u still in Q:
		             alt ← dist[u] + Graph.Edges(u, v)
		              if alt < dist[v]:
		                 dist[v] ← alt
		                prev[v] ← u

		      return dist[], prev[]*/

	w := len(fields[0])
	h := len(fields)

	distances := make(map[vec2]int)

	for y, line := range fields {
		for x := range line {
			distances[vec2{x, y}] = w * h
		}
	}

	parents := make(map[vec2]vec2)
	closedSet := make(map[vec2]bool)
	openSet := make(map[vec2]int)
	openSet[start] = 0
	distances[start] = 0

	for len(openSet) > 0 {
		current := getCurrent(openSet)

		neighbors := getNeighbors2(fields, current)

		for _, neighbor := range neighbors {
			if fields[neighbor.y][neighbor.x] != "#" && !closedSet[neighbor] {
				_, exists := openSet[neighbor]
				altDist := distances[current] + 1
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
		delete(openSet, current)

		closedSet[current] = true

	}

	return distances, parents

}

func getHistory2(parents map[vec2]vec2, target vec2) []vec2 {
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

func part1() { /*
		width := 7
		height := 7

		start := vec2{0, 0}
		end := vec2{6, 6}

		rounds := 12
	*/

	width := 71
	height := 71

	start := vec2{0, 0}
	end := vec2{70, 70}

	//rounds := 1024
	//rounds := 2450
	//rounds := 2700
	//rounds := 2850
	//rounds := 2950
	rounds := 2954
	//rounds := 2975
	//rounds := 3000
	//rounds := 3450

	fields := readMap(width, height, rounds)

	fields[end.y][end.x] = "E"

	_, parents := dijkstra2(fields, start)

	history := getHistory2(parents, end)

	for _, item := range history {
		fields[item.y][item.x] = "O"
	}

	for _, line := range fields {
		fmt.Println(line)
	}

	fmt.Println(len(history))

}

func main() {
	part1()
}
