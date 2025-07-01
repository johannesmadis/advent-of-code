package main

import (
	"fmt"
	"os"
	"strings"
)

func transpose(slice []string) [][]string {
	xl := len(slice[0])
	yl := len(slice)
	result := make([][]string, xl)
	for i := range result {
		result[i] = make([]string, yl)
	}
	for i := 0; i < xl; i++ {
		for j := 0; j < yl; j++ {
			result[i][j] = string(slice[j][i])
		}
	}
	return result
}

func matches(lock []int, key []int) bool {
	limit := 7

	for i, l := range lock {
		if l+key[i] > limit {
			return false
		}
	}

	return true
}

func part1() {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)
	items := strings.Split(inputStr, "\n\n")

	locks := [][]int{}
	keys := [][]int{}

	for _, item := range items {
		isLock := item[0] == '#'
		itemLines := strings.Split(item, "\n")
		transposedItem := transpose(itemLines)

		sums := []int{}
		for _, col := range transposedItem {
			length := 0

			for _, row := range col {
				if row == "#" {
					length++
				}
			}
			sums = append(sums, length)
		}
		if isLock {
			locks = append(locks, sums)
		} else {
			keys = append(keys, sums)
		}
	}

	pairs := 0

	for _, lock := range locks {
		for _, key := range keys {
			if matches(lock, key) {
				pairs++
			}
		}
	}

	fmt.Println(pairs)
}
func main() {
	part1()
}
