package main

import (
	"fmt"
	"os"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func get_input() []string {
	dat, err := os.ReadFile("./input.txt")
	check(err)

	pairs := strings.Split(string(dat), "\n")

	return pairs
}

func checkLine(fields []string) bool {
	deltaPositive := true
	for index, item := range fields[1:] {

		itemA, err := strconv.Atoi(fields[index])
		check(err)
		itemB, err := strconv.Atoi(item)
		check(err)

		if index == 0 {
			// configure delta
			deltaPositive = itemB > itemA
		}

		if deltaPositive {

			if (itemB-itemA) > 3 || (itemA-itemB) >= 0 {
				return false
			}
		} else {

			if (itemA-itemB) > 3 || (itemB-itemA) >= 0 {
				return false
			}
		}
	}
	return true
}

func main() {
	lines := get_input()

	var safesum = 0

	for row, line := range lines {
		fields := strings.Fields(line)

		safe := checkLine(fields)

		if !safe {
			for index := range len(fields) {
				// create a new array to not mutate original
				currentArray := make([]string, len(fields))
				copy(currentArray, fields)

				currentSlice := currentArray[:index]
				dampenedFields := append(currentSlice, currentArray[index+1:]...)
				isDampenedSafe := checkLine(dampenedFields)
				fmt.Println(fields, index, dampenedFields, isDampenedSafe)
				if isDampenedSafe {
					safe = true
					break
				}
			}
		}

		if safe == true {
			safesum += 1
		}
		fmt.Println(row, safe)
	}

	fmt.Println(safesum)

}
