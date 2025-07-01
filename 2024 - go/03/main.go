package main

import (
	"fmt"
	"os"
	"regexp"
	"strconv"
)

func check(e error) {
	if e != nil {
		panic(e)
	}
}

func get_input() string {
	dat, err := os.ReadFile("./input.txt")
	check(err)

	return string(dat)
}

func part1(input string) {

	r, _ := regexp.Compile(`(mul\(\d+,\d+\))`)
	mul, _ := regexp.Compile(`(\d+)`)

	slices := r.FindAllString(input, -1)

	sum := 0
	for _, slice := range slices {
		items := mul.FindAllString(slice, -1)
		a, _ := strconv.Atoi(items[0])
		b, _ := strconv.Atoi(items[1])
		result := a * b
		sum += result
	}
	fmt.Println(sum)
}

func part2(input string) {
	r, _ := regexp.Compile(`(mul\(\d+,\d+\)|do\(\)|don't\(\))`)
	mul, _ := regexp.Compile(`(\d+)`)

	slices := r.FindAllString(input, -1)

	filtered := []string{}

	enabled := true
	for _, item := range slices {
		if item == "do()" {
			enabled = true
			continue
		}
		if item == "don't()" {
			enabled = false
			continue
		}

		if enabled {
			filtered = append(filtered, item)
		}

	}

	sum := 0
	for _, slice := range filtered {
		items := mul.FindAllString(slice, -1)
		a, _ := strconv.Atoi(items[0])
		b, _ := strconv.Atoi(items[1])
		result := a * b
		sum += result
	}
	fmt.Println(sum)
}

func main() {
	input := get_input()

	part1(input)
	part2(input)
}
