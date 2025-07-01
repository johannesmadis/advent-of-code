package main

import (
	"fmt"
	"os"
	"regexp"
	"strings"
)

func part1() {

	input, _ := os.ReadFile("./input.txt")
	inputs := strings.Split(string(input), "\n\n")
	patterns := strings.Split(inputs[0], ", ")
	designs := strings.Split(inputs[1], "\n")

	re, _ := regexp.Compile("^(" + strings.Join(patterns, "|") + ")+$")

	sum := 0
	for _, design := range designs {
		if re.MatchString(design) {
			sum++
		}
	}

	fmt.Println(sum)
}

func cachedCombinations(cacheRef *map[string]int, patternExpressions []regexp.Regexp, input string) int {
	cache := *cacheRef
	cachedResult, exists := cache[input]
	if exists {
		return cachedResult
	}

	result := findCombinations(cacheRef, patternExpressions, input)
	return result
}

func findCombinations(cacheRef *map[string]int, patternExpressions []regexp.Regexp, input string) int {
	cache := *cacheRef
	result := 0
	for _, exp := range patternExpressions {
		nextStr := exp.ReplaceAllString(input, "")

		if nextStr == "" {
			result += 1
		} else if nextStr != input {
			localResult := cachedCombinations(cacheRef, patternExpressions, nextStr)
			cache[nextStr] = localResult

			result += localResult
		}

	}
	return result
}
func part2() {
	input, _ := os.ReadFile("./input.txt")
	inputs := strings.Split(string(input), "\n\n")
	patterns := strings.Split(inputs[0], ", ")
	designs := strings.Split(inputs[1], "\n")

	//patternsMap := make(map[string]bool)
	patternExpressions := []regexp.Regexp{}

	for _, pattern := range patterns {
		patternExpressions = append(patternExpressions, *regexp.MustCompile("^" + pattern))
	}

	// find all matches where string starts with anything from patterns regex
	// for all matches, find all matches of remaining substrings where string start matches regex
	// continue until no remainder. If remainder doesnt match, current combination does not get added If no remainder, combination sum gets added

	sum := 0
	cache := make(map[string]int)
	for _, design := range designs {

		sum += cachedCombinations(&cache, patternExpressions, design)

	}

	fmt.Println(sum)
}
func main() {
	part1()
	part2()
}
