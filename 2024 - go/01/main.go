package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func main() {
	dat, err := os.ReadFile("./input.txt")
	check(err)

	fmt.Print(string(dat))

	pairs := strings.Split(string(dat), "\n")

	var arrA [1000]int
	var arrB [1000]int

	for index, pair := range pairs {
		fmt.Println(pair)
		words := strings.Fields(pair)

		a, err := strconv.Atoi(words[0])
		check(err)

		b, err := strconv.Atoi(words[1])
		check(err)

		arrA[index] = a
		arrB[index] = b

	}

	aSlice := arrA[0:1000]
	bSlice := arrB[0:1000]

	slices.Sort(aSlice)
	slices.Sort(bSlice)

	sum := 0

	for index := range 1000 {
		a := aSlice[index]
		b := bSlice[index]

		var distance int

		if a > b {
			distance = a - b
		} else {
			distance = b - a
		}
		fmt.Println(distance)
		sum += distance
	}

	fmt.Print(sum)

	// part 2

	similarity := 0

	for _, keyA := range aSlice {
		current := 0
		fmt.Println(keyA)

		for _, keyB := range bSlice {

			if keyA == keyB {
				current += 1
			}
		}
		similarity += keyA * current
	}

	fmt.Print(similarity)

}
