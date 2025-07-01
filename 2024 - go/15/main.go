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

func tryMove(x int, y int, dir vec2, warehouseRef *[][]string) bool {
	nextX := x + dir.x
	nextY := y + dir.y

	warehouse := *warehouseRef

	if warehouse[nextY][nextX] == "#" {
		return false
	}

	if warehouse[nextY][nextX] == "." {
		// move in warehouse
		warehouse[nextY][nextX] = warehouse[y][x]
		warehouse[y][x] = "."
		return true
	}

	if (warehouse[nextY][nextX]) == "O" {
		result := tryMove(nextX, nextY, dir, warehouseRef)
		if result {
			warehouse[nextY][nextX] = warehouse[y][x]
			warehouse[y][x] = "."
			return true
		}
	}

	return false
}

func displayWarehouse(warehouse [][]string) {
	for _, line := range warehouse {
		lineStr := strings.Join(line, "")
		fmt.Println(lineStr)
	}
}

func part1() {
	input, _ := os.ReadFile("input.txt")
	inputStr := string(input)

	parts := strings.Split(inputStr, "\n\n")
	warehouse := [][]string{}
	inputMoves := []string{}

	currentX := -1
	currentY := -1

	for y, line := range strings.Split(parts[0], "\n") {
		items := strings.Split(line, "")
		for x, item := range items {
			if item == "@" {
				currentX = x
				currentY = y
			}
		}
		warehouse = append(warehouse, items)
	}

	for _, line := range strings.Split(parts[1], "\n") {
		items := strings.Split(line, "")
		inputMoves = append(inputMoves, items...)
	}

	for _, input := range inputMoves {
		dir := vec2{0, 0}

		if input == ">" {
			dir.x = 1

		}
		if input == "<" {
			dir.x = -1
		}
		if input == "^" {
			dir.y = -1
		}
		if input == "v" {
			dir.y = 1
		}
		result := tryMove(currentX, currentY, dir, &warehouse)
		if result {
			currentX += dir.x
			currentY += dir.y
		}
		//displayWarehouse(warehouse)

	}

	displayWarehouse(warehouse)

	sum := 0

	for y, line := range warehouse {
		for x, item := range line {
			if item == "O" {
				sum += 100*y + x
			}
		}
	}

	fmt.Println(sum)

}

func tryMoveWide(x int, y int, dir vec2, warehouseRef *[][]string) (bool, []move) {
	nextX := x + dir.x
	nextY := y + dir.y

	resultMoves := []move{}
	dummyMoves := []move{}

	warehouse := *warehouseRef
	currentItem := warehouse[y][x]

	nextItem := warehouse[nextY][nextX]

	// horizontal movement
	if (nextItem == "[" || nextItem == "]") && dir.y == 0 {
		result, moves := tryMoveWide(nextX, nextY, dir, warehouseRef)
		if result {
			resultMoves = append(resultMoves, moves...)
			resultMoves = append(resultMoves, move{vec2{nextX, nextY}, currentItem})
			resultMoves = append(resultMoves, move{vec2{x, y}, "."})

			return true, resultMoves
		}
		return false, dummyMoves
	}

	if dir.y != 0 && nextItem == "[" {

		result0, moves0 := tryMoveWide(nextX, nextY, dir, warehouseRef)
		result1, moves1 := tryMoveWide(nextX+1, nextY, dir, warehouseRef)

		if result0 && result1 {
			resultMoves = append(resultMoves, moves0...)
			resultMoves = append(resultMoves, moves1...)

			resultMoves = append(resultMoves, move{vec2{nextX, nextY}, currentItem})
			resultMoves = append(resultMoves, move{vec2{x, y}, "."})

			return true, resultMoves
		}
		return false, dummyMoves
	}

	if (dir.y != 0) && (nextItem == "]") {
		result0, moves0 := tryMoveWide(x, nextY, dir, warehouseRef)
		result1, moves1 := tryMoveWide(x-1, nextY, dir, warehouseRef)
		if result0 && result1 {

			resultMoves = append(resultMoves, moves0...)
			resultMoves = append(resultMoves, moves1...)

			resultMoves = append(resultMoves, move{vec2{nextX, nextY}, currentItem})
			resultMoves = append(resultMoves, move{vec2{x, y}, "."})

			return true, resultMoves
		}
		return false, dummyMoves
	}

	if nextItem == "#" {
		return false, dummyMoves
	}

	if nextItem == "." {
		// move in warehouse
		resultMoves = append(resultMoves, move{vec2{nextX, nextY}, currentItem})
		resultMoves = append(resultMoves, move{vec2{x, y}, "."})
		return true, resultMoves
	}
	return false, dummyMoves
}

type move struct {
	target vec2
	value  string
}

func part2() {
	input, _ := os.ReadFile("input.txt")
	inputStr := string(input)

	parts := strings.Split(inputStr, "\n\n")
	warehouse := [][]string{}
	inputMoves := []string{}

	currentX := -1
	currentY := -1

	// map
	for y, line := range strings.Split(parts[0], "\n") {
		items := strings.Split(line, "")
		widerLine := []string{}
		for x, item := range items {
			if item == "@" {
				currentX = x * 2
				currentY = y
				widerLine = append(widerLine, item, ".")

			} else if item == "O" {
				widerLine = append(widerLine, "[", "]")

			} else {
				widerLine = append(widerLine, item, item)
			}
		}
		warehouse = append(warehouse, widerLine)
	}

	displayWarehouse(warehouse)

	for _, line := range strings.Split(parts[1], "\n") {
		items := strings.Split(line, "")
		inputMoves = append(inputMoves, items...)
	}

	for _, input := range inputMoves {
		dir := vec2{0, 0}

		if input == ">" {
			dir.x = 1

		}
		if input == "<" {
			dir.x = -1
		}
		if input == "^" {
			dir.y = -1
		}
		if input == "v" {
			dir.y = 1
		}
		result, moves := tryMoveWide(currentX, currentY, dir, &warehouse)

		if result {
			for _, move := range moves {
				if move.value == "." {
					warehouse[move.target.y][move.target.x] = move.value

				}
			}

			for _, move := range moves {
				if move.value != "." {
					warehouse[move.target.y][move.target.x] = move.value
				}
			}

			currentX += dir.x
			currentY += dir.y
		}

		//displayWarehouse(warehouse)

		//bufio.NewReader(os.Stdin).ReadBytes('\n')

	}

	displayWarehouse(warehouse)

	sum := 0

	for y, line := range warehouse {
		for x, item := range line {
			if item == "[" {
				sum += 100*y + x
			}
		}
	}

	fmt.Println(sum)
}

func main() {
	part1()
	part2()
}
