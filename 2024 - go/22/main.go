package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func mix(a int, b int) int {
	return a ^ b // XOR
}
func prune(a int) int {
	return a % 16777216 // MOD pow 2 24
}

func sequence(prev int) int {
	next := mix(prev*64, prev)
	next = prune(next)

	next = mix(next/32, next)
	next = prune(next)

	next = mix(next*2048, next)
	next = prune(next)

	return next
}

func part1() {

	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	lines := strings.Split(inputStr, "\n")

	inputs := []int{}

	for _, line := range lines {
		val, _ := strconv.Atoi(line)
		inputs = append(inputs, val)
	}

	sum := 0
	for _, input := range inputs {
		currentInput := input
		for i := 0; i < 2000; i++ {
			currentInput = sequence(currentInput)
		}
		//fmt.Println(currentInput)
		sum += currentInput
	}

	fmt.Println(sum)
}

type vec4 struct {
	a int
	b int
	c int
	d int
}

func (v vec4) stringify() string {
	return strconv.Itoa(v.a) + "," + strconv.Itoa(v.b) + "," + strconv.Itoa(v.c) + "," + strconv.Itoa(v.d)
}

func part2() {

	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	lines := strings.Split(inputStr, "\n")

	inputs := []int{}

	for _, line := range lines {
		val, _ := strconv.Atoi(line)
		inputs = append(inputs, val)
	}

	// -9 .. 0 .. 9
	sequences := make(map[string]int)

	// for each sequence make a

	//since := time.Now()
	for _, input := range inputs {
		//fmt.Println(time.Since(since))
		//since = time.Now()

		currentInput := sequence(input)
		prevInput := input
		sequenceVec := vec4{}

		usedSequences := make(map[string]bool)
		for i := 0; i < 2000; i++ {

			prevLast := prevInput % 10
			currentLast := currentInput % 10

			//fmt.Println(currentInput, currentLast, price, delta)

			//fmt.Println(nextInput, currentInput, delta)

			sequenceVec.a = sequenceVec.b
			sequenceVec.b = sequenceVec.c
			sequenceVec.c = sequenceVec.d
			sequenceVec.d = currentLast - prevLast

			if i > 2 && !usedSequences[sequenceVec.stringify()] {

				sequences[sequenceVec.stringify()] += currentLast
				usedSequences[sequenceVec.stringify()] = true
			}

			prevInput = currentInput
			currentInput = sequence(currentInput)

		}
		//fmt.Println(currentInput)
	}

	max_sum := 0
	s := ""

	for seq, sum := range sequences {
		if max_sum < sum {
			max_sum = sum
			s = seq
		}
	}

	fmt.Println(s, max_sum)
	fmt.Println(sequences["0,0,-1,1"])
}

func main() {
	part1()
	part2()
}
