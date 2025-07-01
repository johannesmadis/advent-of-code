package main

import (
	"fmt"
	"math"
	"strconv"
	"strings"
)

func parseField(input int) int {
	if input == 0 {
		return 1
	}

	return input * 2024
}

type vec2 struct {
	x int
	y int
}

func part1(numberStr []string) {

	numberSlice := []float64{}
	for _, item := range numberStr {
		numberFloat, _ := strconv.ParseFloat(item, 64)
		numberSlice = append(numberSlice, numberFloat)
	}

	n := 25
	for i := 0; i < n; i++ {
		appendables := []float64{}
		for index, item := range numberSlice {
			decimalCount := int(math.Floor(math.Log10(item))) + 1

			if item == 0 {
				numberSlice[index] = 1
				continue
			}
			if decimalCount%2 == 0 {
				// 123456 to 123 and 456

				firstPart := math.Floor(item / math.Pow10(decimalCount/2))
				numberSlice[index] = firstPart

				secondPart := item - firstPart*math.Pow10(decimalCount/2)

				appendables = append(appendables, secondPart)
				//
				continue
			}
			numberSlice[index] = item * 2024

		}
		numberSlice = append(numberSlice, appendables...)
		//fmt.Println(numberSlice)
	}

	fmt.Println(len(numberSlice))
}

func part2(numberStr []string) {

	frequencyMap := make(map[int]int)

	// register initials
	for _, item := range numberStr {
		number, _ := strconv.Atoi(item)

		frequencyMap[number] += 1
	}
	// loop

	for i := 0; i < 75; i++ {
		tempFrequencyMap := make(map[int]int)
		for k, v := range frequencyMap {
			tempFrequencyMap[k] = v
		}

		for item, value := range frequencyMap {
			if value == 0 {
				continue
			}
			if item == 0 {
				tempFrequencyMap[1] += value
				tempFrequencyMap[0] -= value
				continue
			}

			decimalCount := int(math.Floor(math.Log10(float64(item)))) + 1

			if decimalCount%2 == 0 {
				first := int(math.Floor(float64(item) / math.Pow10(decimalCount/2)))
				second := int(float64(item) - float64(first)*math.Pow10(decimalCount/2))

				tempFrequencyMap[first] += value

				tempFrequencyMap[second] += value
				tempFrequencyMap[item] -= value

				continue
			}

			tempFrequencyMap[item*2024] += value
			tempFrequencyMap[item] -= value

		}
		frequencyMap = tempFrequencyMap

	}

	sum := 0
	for _, item := range frequencyMap {
		sum += item
	}
	fmt.Println(sum)
}

func main() {
	input := "5 127 680267 39260 0 26 3553 5851995"
	//input := "125 17"
	numberStr := strings.Fields(input)

	part1(numberStr)

	part2(numberStr)

}
