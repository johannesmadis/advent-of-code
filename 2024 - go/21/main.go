package main

import (
	"fmt"
	"strconv"
	"strings"
)

type vec2 struct {
	x int
	y int
}

func absInt(a int) int {
	if a < 0 {
		return -a
	}
	return a
}
func manhattan(a vec2, b vec2) int {
	return absInt(b.x-a.x) + absInt(b.y-a.y)
}

type cachedResult struct {
	pos    vec2
	result int
}

func cachedRecursiveRouter(
	cache map[string]map[vec2]map[int]cachedResult,
	layout map[string]vec2,
	target string,
	pos vec2,
	robotCount int) (int, vec2) {

	cached, exists := cache[target][pos][robotCount]
	if exists {
		return cached.result, cached.pos
	}

	result, resultPos := recursiveRouter(cache, layout, target, pos, robotCount)

	_, targetExists := cache[target]
	if !targetExists {
		cache[target] = make(map[vec2]map[int]cachedResult)
	}

	_, posExists := cache[target][pos]
	if !posExists {
		cache[target][pos] = make(map[int]cachedResult)
	}

	cache[target][pos][robotCount] = cachedResult{resultPos, result}

	return result, resultPos

}

func recursiveRouter(cache map[string]map[vec2]map[int]cachedResult, layout map[string]vec2, target string, pos vec2, robotCount int) (int, vec2) {

	//fmt.Println("Starting pos", target, pos)
	arrowKbPos := map[string]vec2{
		"-1": {0, 0},
		"^":  {1, 0},
		"A":  {2, 0},
		"<":  {0, 1},
		"v":  {1, 1},
		">":  {2, 1},
	}
	// find route to next nr both horizontal first and vertical first
	// add A
	// if another robot does that, feed to another robot and return its length
	// otherwise return smaller of vertical or horizontal length

	targetPos := layout[target]

	dX := targetPos.x - pos.x
	dY := targetPos.y - pos.y

	horizontalProblem := layout["-1"] == vec2{targetPos.x, pos.y}
	verticalProblem := layout["-1"] == vec2{pos.x, targetPos.y}

	//fmt.Println(horizontalProblem, verticalProblem)

	horizontal := []string{}
	vertical := []string{}

	for range absInt(dX) {
		char := ">"

		if dX < 0 {
			char = "<"
		}
		horizontal = append(horizontal, char)
	}
	for range absInt(dY) {
		char := "v"
		if dY < 0 {
			char = "^"
		}
		vertical = append(vertical, char)
	}

	combo := []string{}
	combo = append(combo, vertical...)
	combo = append(combo, horizontal...)
	combo = append(combo, "A")
	//fmt.Println(combo)

	result := 0
	if robotCount > 0 {
		// horizontal first
		horizontalFirst := []string{}
		horizontalFirst = append(horizontalFirst, horizontal...)
		horizontalFirst = append(horizontalFirst, vertical...)
		horizontalFirst = append(horizontalFirst, "A")

		horizontalSum := 0
		currentHPos := arrowKbPos["A"]
		for _, target := range horizontalFirst {
			currentSum, currentPos := cachedRecursiveRouter(cache, arrowKbPos, target, currentHPos, robotCount-1)
			horizontalSum += currentSum
			currentHPos = currentPos
		}

		// vertical first
		verticalFirst := []string{}
		verticalFirst = append(verticalFirst, vertical...)
		verticalFirst = append(verticalFirst, horizontal...)
		verticalFirst = append(verticalFirst, "A")

		verticalSum := 0
		currentVPos := arrowKbPos["A"]
		for _, target := range verticalFirst {
			verticalTempSum, currentPos := cachedRecursiveRouter(cache, arrowKbPos, target, currentVPos, robotCount-1)
			verticalSum += verticalTempSum
			currentVPos = currentPos

		}

		if verticalProblem {
			result += horizontalSum
		} else if horizontalProblem {
			result += verticalSum
		} else if horizontalSum < verticalSum {
			result += horizontalSum
		} else {
			result += verticalSum
		}

	} else {
		result += len(vertical) + len(horizontal) + 1 // +1 for A
	}

	return result, targetPos

}

func main() {
	//part1()
	mainKbPos := map[string]vec2{
		"7":  {0, 0},
		"8":  {1, 0},
		"9":  {2, 0},
		"4":  {0, 1},
		"5":  {1, 1},
		"6":  {2, 1},
		"1":  {0, 2},
		"2":  {1, 2},
		"3":  {2, 2},
		"-1": {0, 3},
		"0":  {1, 3},
		"A":  {2, 3},
	}

	inputStr := []string{
		/*"029A",
		"980A",
		"179A",
		"456A",
		"379A",*/

		"973A",
		"836A",
		"780A",
		"985A",
		"413A",
	}

	inputs := [][]string{}
	for _, line := range inputStr {
		lineArr := strings.Split(line, "")

		inputs = append(inputs, lineArr)
	}

	cache := make(map[string]map[vec2]map[int]cachedResult) // target, pos, robotCount

	total := 0
	for _, input := range inputs {
		lineVal := strings.Join(input[:3], "")
		lineInt, _ := strconv.Atoi(lineVal)

		sum := 0
		pos := mainKbPos["A"]

		for _, item := range input {

			currentSum, currentPos := recursiveRouter(cache, mainKbPos, item, pos, 25)
			sum += currentSum
			pos = currentPos
		}

		//fmt.Println(lineInt, sum, lineInt*sum)
		total += lineInt * sum

	}
	fmt.Println(total)

}
