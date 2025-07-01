package main

import (
	"fmt"
	"os"
	"slices"
	"strings"
)

func readInput() [][]string {
	input, _ := os.ReadFile("./input.txt")
	inputLines := strings.Split(string(input), "\n")

	result := [][]string{}

	for _, line := range inputLines {
		currentLine := []string{}
		for _, char := range strings.Split(line, "") {
			currentLine = append(currentLine, char)
		}
		result = append(result, currentLine)
	}

	return result
}

type metaPt struct {
	x       int
	y       int
	id      string
	groupId int
}

type vec2 struct {
	x int
	y int
}

func floodFill(groupIdMap *map[vec2]int, input [][]string, pos vec2, groupId int) {

	height := len(input)
	width := len(input[0])

	targetMap := *groupIdMap

	currentValue := input[pos.y][pos.x]

	targetMap[pos] = groupId

	neighbors := []vec2{{pos.x + 1, pos.y}, {pos.x - 1, pos.y}, {pos.x, pos.y + 1}, {pos.x, pos.y - 1}}

	for _, n := range neighbors {
		if n.x >= 0 && n.y >= 0 && n.x < width && n.y < height {
			value := input[n.y][n.x]
			_, targetGroupIdExists := targetMap[n]
			if value == currentValue && !targetGroupIdExists {
				floodFill(groupIdMap, input, n, groupId)
			}
		}

	}

}

func getRegionMap(input [][]string) map[int][]vec2 {
	currentGroupId := -1
	groupIdMap := make(map[vec2]int)

	for y, row := range input {
		for x := range row {

			index := vec2{x, y}
			_, exists := groupIdMap[index]

			if exists {
				continue
			} else {
				currentGroupId++
				groupIdMap[index] = currentGroupId
				floodFill(&groupIdMap, input, index, currentGroupId)
			}

		}
	}

	regionMap := make(map[int][]vec2)

	for vec, groupId := range groupIdMap {
		list := regionMap[groupId]
		list = append(list, vec)
		regionMap[groupId] = list
	}

	return regionMap
}

func getPerimeter(input [][]string, vecs []vec2) []vec2 {
	perimeter := []vec2{}
	height := len(input)
	width := len(input[0])

	for _, vec := range vecs {
		vecValue := input[vec.y][vec.x]

		if vec.x == 0 || vec.y == 0 || vec.x == width-1 || vec.y == height-1 {
			perimeter = append(perimeter, vec)
			continue
		}

		neighbors := []vec2{
			{vec.x + 1, vec.y},
			{vec.x - 1, vec.y},
			{vec.x, vec.y + 1},
			{vec.x, vec.y - 1},
		}

		for _, n := range neighbors {
			value := input[n.y][n.x]

			if value != vecValue {
				perimeter = append(perimeter, vec)
				break
			}
		}

	}
	return perimeter
}

func part1() {

	input := readInput()

	// loop through each item in input
	// if input coords has groupId, skip
	// else recursevly loop through point and neighbours (flood fill)
	// to assign groupId to each point
	// continue

	regionMap := getRegionMap(input)

	height := len(input)
	width := len(input[0])

	sum := 0

	for _, vecs := range regionMap {
		regionArea := 0

		perimeterCount := 0

		for _, vec := range vecs {
			regionArea++
			vecValue := input[vec.y][vec.x]

			neighbors := []vec2{
				{vec.x + 1, vec.y},
				{vec.x - 1, vec.y},
				{vec.x, vec.y + 1},
				{vec.x, vec.y - 1},
			}

			for _, n := range neighbors {
				var value string
				if n.x >= 0 && n.y >= 0 && n.x < width && n.y < height {
					value = input[n.y][n.x]

				}
				if value != vecValue {
					perimeterCount++
				}
			}

		}
		sum += regionArea * perimeterCount

	}

	fmt.Println("sum", sum)

}

func makeSideArrayMap(inputMap map[int]map[int]bool) int {
	sideArrays := make(map[int][]int)

	for a, b := range inputMap {
		sideArray := sideArrays[a]
		for c := range b {
			sideArray = append(sideArray, c)
		}
		sideArrays[a] = sideArray
	}

	result := 0
	for _, arr := range sideArrays {
		slices.Sort(arr)

		sideCount := 1
		for index, key := range arr {
			if index == 0 {
				continue
			}
			if arr[index-1] != key-1 {
				sideCount++
			}
		}
		result += sideCount
	}

	return result

}

func getPerimeterLines(input [][]string, points []vec2) int {
	height := len(input)
	width := len(input[0])

	xupMap := make(map[int]map[int]bool)    // first int is y
	xdownMap := make(map[int]map[int]bool)  // first int is y
	yleftMap := make(map[int]map[int]bool)  // first int is x
	yrightMap := make(map[int]map[int]bool) // first int is x

	for _, item := range points {
		value := input[item.y][item.x]

		if item.y == 0 || input[item.y-1][item.x] != value {
			_, exists := xupMap[item.y]
			if !exists {
				xupMap[item.y] = make(map[int]bool)
			}
			xupMap[item.y][item.x] = true
		}
		if item.y == height-1 || input[item.y+1][item.x] != value {
			_, exists := xdownMap[item.y]
			if !exists {
				xdownMap[item.y] = make(map[int]bool)
			}
			xdownMap[item.y][item.x] = true
		}

		if item.x == 0 || input[item.y][item.x-1] != value {
			_, exists := yleftMap[item.x]
			if !exists {
				yleftMap[item.x] = make(map[int]bool)
			}
			yleftMap[item.x][item.y] = true
		}
		if item.x == width-1 || input[item.y][item.x+1] != value {
			_, exists := yrightMap[item.x]
			if !exists {
				yrightMap[item.x] = make(map[int]bool)
			}
			yrightMap[item.x][item.y] = true
		}

	}

	sideArraysYLeft := makeSideArrayMap(yleftMap)
	sideArraysYRight := makeSideArrayMap(yrightMap)
	sideArraysXUp := makeSideArrayMap(xupMap)
	sideArraysXDown := makeSideArrayMap(xdownMap)

	sideCountSum := sideArraysXDown + sideArraysXUp + sideArraysYLeft + sideArraysYRight

	return sideCountSum

}

func part2() {

	input := readInput()
	regionMap := getRegionMap(input)
	sum := 0
	for _, vecs := range regionMap {
		perimeter := getPerimeter(input, vecs)

		sideCount := getPerimeterLines(input, perimeter)
		sum += len(vecs) * sideCount
	}

	fmt.Println("part2", sum)

}

func main() {
	part1()
	part2()

}
