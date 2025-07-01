package main

import (
	"fmt"
	"log"
	"os"
	"strconv"
	"strings"
	"time"
)

func readInput() []string {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)
	lines := strings.Split(inputStr, "\n")

	return lines
}

func concat(a int, b int) int {
	if b >= 100 {
		return a*1000 + b
	}
	if b >= 10 {
		return a*100 + b
	}
	return a*10 + b
}

func recursiveOperation(a int, operands []int, index int, intendedResult int) bool {
	tempAddition := a + operands[index]
	tempMultiplication := a * operands[index]
	tempConcatenation := concat(a, operands[index])

	if index == (len(operands) - 1) {
		return tempAddition == intendedResult || tempConcatenation == intendedResult || tempMultiplication == intendedResult

	}

	r1 := recursiveOperation(tempAddition, operands, index+1, intendedResult)
	if r1 {
		return r1
	}

	r2 := recursiveOperation(tempMultiplication, operands, index+1, intendedResult)
	if r2 {
		return r2
	}
	r3 := recursiveOperation(tempConcatenation, operands, index+1, intendedResult)

	return r3

}

func part1() {
	lines := readInput()

	sum := 0
	for _, line := range lines {
		parts := strings.Split(line, ": ")
		intendedResult, _ := strconv.Atoi(parts[0])
		intendedOperandStrings := strings.Fields(parts[1])

		intendedOperands := []int{}
		for _, operandString := range intendedOperandStrings {
			intendedOperand, _ := strconv.Atoi(operandString)
			intendedOperands = append(intendedOperands, intendedOperand)
		}

		resultExists := recursiveOperation(intendedOperands[0], intendedOperands, 1, intendedResult)

		if resultExists {
			sum += intendedResult
		}
	}

	fmt.Println(sum)

}

func part2() {}

func main() {
	start := time.Now()

	part1()
	part2()
	elapsed := time.Since(start)
	log.Printf("Binomial took %s", elapsed)
}
