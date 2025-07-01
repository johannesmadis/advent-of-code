package main

import (
	"fmt"
	"os"
	"strings"
)

func getInput() []string {
	dat, _ := os.ReadFile("./input.txt")
	return strings.Split(string(dat), "\n")
}

func countXMAS(input []string, rowIndex int, charIndex int) int {
	rowLength := len(input[0])
	counter := 0

	fitsForward := rowLength-charIndex >= 4
	fitsBackward := charIndex >= 3
	fitsUp := rowIndex >= 3
	fitsDown := len(input)-rowIndex >= 4
	// ltr

	if fitsForward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex][charIndex+1]) + string(input[rowIndex][charIndex+2]) + string(input[rowIndex][charIndex+3])
		if tempString == "XMAS" {
			counter += 1
		}
	}

	// rtl
	if fitsBackward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex][charIndex-1]) + string(input[rowIndex][charIndex-2]) + string(input[rowIndex][charIndex-3])
		if tempString == "XMAS" {
			counter += 1
		}
	}

	// btt

	if fitsUp {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex-1][charIndex]) + string(input[rowIndex-2][charIndex]) + string(input[rowIndex-3][charIndex])
		if tempString == "XMAS" {
			counter += 1
		}
	}
	// ttb

	if fitsDown {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex+1][charIndex]) + string(input[rowIndex+2][charIndex]) + string(input[rowIndex+3][charIndex])
		if tempString == "XMAS" {
			counter += 1
		}

	}

	if fitsUp && fitsForward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex-1][charIndex+1]) + string(input[rowIndex-2][charIndex+2]) + string(input[rowIndex-3][charIndex+3])
		if tempString == "XMAS" {
			counter += 1
		}
	}
	// diagonal right up

	// diagonal right down
	if fitsDown && fitsForward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex+1][charIndex+1]) + string(input[rowIndex+2][charIndex+2]) + string(input[rowIndex+3][charIndex+3])
		if tempString == "XMAS" {
			counter += 1
		}
	}
	// diagonal left up
	if fitsUp && fitsBackward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex-1][charIndex-1]) + string(input[rowIndex-2][charIndex-2]) + string(input[rowIndex-3][charIndex-3])
		if tempString == "XMAS" {
			counter += 1
		}
	}
	// diagonal left down
	if fitsDown && fitsBackward {
		tempString := string(input[rowIndex][charIndex]) + string(input[rowIndex+1][charIndex-1]) + string(input[rowIndex+2][charIndex-2]) + string(input[rowIndex+3][charIndex-3])
		if tempString == "XMAS" {
			counter += 1
		}
	}

	return counter
}

func countMAS(input []string, rI int, cI int) int {
	rowLength := len(input[0])

	counter := 0

	fitsForward := rowLength-cI > 1
	fitsBackward := cI > 0
	fitsUp := rI > 0
	fitsDown := len(input)-rI > 1

	if fitsBackward && fitsForward && fitsUp && fitsDown {
		diagonalUpLeft := string(input[rI+1][cI-1]) + string(input[rI][cI]) + string(input[rI-1][cI+1])
		diagonalDownLeft := string(input[rI-1][cI-1]) + string(input[rI][cI]) + string(input[rI+1][cI+1])
		if (diagonalDownLeft == "MAS" || diagonalDownLeft == "SAM") && (diagonalUpLeft == "MAS" || diagonalUpLeft == "SAM") {
			counter += 1
		}
	}

	return counter
}

func part1() {
	// find each xmas and samx for both input and transposed input
	input := getInput()

	// for each char in each row, if its X, count how many XMASes it provides
	// and add to counter

	counter := 0

	for rI, row := range input {
		for cI, char := range row {
			if char == 'X' {
				counter += countXMAS(input, rI, cI)
			}
		}
	}

	fmt.Println(counter)

}

func part2() {
	input := getInput()
	counter := 0

	for rI, row := range input {
		for cI, char := range row {
			if char == 'A' {
				counter += countMAS(input, rI, cI)
			}
		}
	}

	fmt.Println(counter)
}

func main() {
	part1()
	part2()
}
