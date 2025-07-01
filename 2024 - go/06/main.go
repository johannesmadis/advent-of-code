package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func readMap() [][]string {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)
	lines := strings.Split(inputStr, "\n")
	fields := [][]string{}
	for _, line := range lines {
		lineSlice := strings.Split(line, "")
		fields = append(fields, lineSlice)
	}
	return fields
}

func turn(currentDirection string) (string, int, int) {
	switch currentDirection {
	case "up":
		return "right", 1, 0
	case "right":
		return "down", 0, 1
	case "down":
		return "left", -1, 0
	}
	// case left, default
	return "up", 0, -1

}

func findGuardPosition(fields [][]string) (int, int) {
	for y, line := range fields {
		for x, char := range line {
			if char == "^" {
				return x, y
			}
		}
	}
	return -1, -1
}

func part1() {
	direction := "up"
	xVel := 0
	yVel := -1

	fields := readMap()
	posX, posY := findGuardPosition(fields)

	mapWidth := len(fields[0])
	mapHeight := len(fields)

	positionsSet := make(map[string]bool)
	positionsSet[strconv.Itoa(posX)+","+strconv.Itoa(posY)] = true

	for true {
		nextPosX := posX + xVel
		nextPosY := posY + yVel
		if nextPosX < 0 || nextPosY < 0 || nextPosX >= mapWidth || nextPosY >= mapHeight {
			break
		}

		nextPos := fields[nextPosY][nextPosX]

		if nextPos == "#" {
			direction, xVel, yVel = turn(direction)
			continue
		}

		posX = nextPosX
		posY = nextPosY
		positionsSet[strconv.Itoa(posX)+","+strconv.Itoa(posY)] = true
	}
	fmt.Println(positionsSet, len(positionsSet))

}

func part2() {
	// its a loop if guard would revisit place with same direction
	// so we save direction as well at position set
	direction := "up"
	xVel := 0
	yVel := -1

	fields := readMap()
	posX, posY := findGuardPosition(fields)
	startX, startY := posX, posY

	mapWidth := len(fields[0])
	mapHeight := len(fields)

	// for each location except starting position try, if loop happens
	// if it does, add to loopset

	loopSet := make(map[string]bool)

	for testY, row := range fields {
		for testX := range row {
			// ignore starting location
			if testX == startX && testY == startY {
				continue
			}

			// reset guard
			posX, posY = startX, startY
			xVel = 0
			yVel = -1
			direction = "up"

			positionsSet := make(map[string]bool)
			positionsSet[strconv.Itoa(posX)+","+strconv.Itoa(posY)+","+direction] = true

			for true {
				nextPosX := posX + xVel
				nextPosY := posY + yVel
				if nextPosX < 0 || nextPosY < 0 || nextPosX >= mapWidth || nextPosY >= mapHeight {
					break
				}

				nextPos := fields[nextPosY][nextPosX]

				// add condition that the testx and y act as obstacle
				if nextPos == "#" || (nextPosX == testX && nextPosY == testY) {
					direction, xVel, yVel = turn(direction)
					continue
				}

				// check for loop
				positionIdentifier := strconv.Itoa(nextPosX) + "," + strconv.Itoa(nextPosY) + "," + direction
				_, exists := positionsSet[positionIdentifier]

				if exists {
					// loop achieved
					loopSet[strconv.Itoa(testX)+","+strconv.Itoa(testY)] = true
					break
				}

				posX = nextPosX
				posY = nextPosY
				positionsSet[positionIdentifier] = true
			}

		}
	}

	fmt.Println(loopSet, len(loopSet))
}
func main() {
	part1()
	part2()
}
