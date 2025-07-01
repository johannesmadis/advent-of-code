package main

import (
	"fmt"
	"maps"
	"os"
	"slices"
	"sort"
	"strings"
)

type link struct {
	a   string
	b   string
	id0 string
	id1 string
}

func part1() {
	input, _ := os.ReadFile("./input.test.txt")
	inputStr := string(input)

	lines := strings.Split(inputStr, "\n")

	lineMap := make(map[string]bool)
	result := make(map[string]bool)

	for _, line := range lines {
		items := strings.Split(line, "-")

		lineMap[line] = true
		lineMap[items[1]+"-"+items[0]] = true
	}

	fmt.Println(lineMap)

	for _, line := range lines {
		items := strings.Split(line, "-")
		itemA := items[0]
		itemB := items[1]

		for _, line2 := range lines {
			items2 := strings.Split(line2, "-")

			itemC := items2[0]
			itemD := items2[1]

			exists := false

			if itemA == itemC && itemB != itemD {
				_, exists0 := lineMap[itemA+"-"+itemD]
				_, exists1 := lineMap[itemB+"-"+itemD]
				exists = exists0 && exists1

			} else if itemA == itemD && itemB != itemC {
				_, exists0 := lineMap[itemA+"-"+itemC]
				_, exists1 := lineMap[itemB+"-"+itemC]
				exists = exists0 && exists1
			} else if itemB == itemC && itemA != itemD {
				_, exists0 := lineMap[itemA+"-"+itemD]
				_, exists1 := lineMap[itemB+"-"+itemD]
				exists = exists0 && exists1
			} else if itemB == itemD && itemA != itemC {
				_, exists0 := lineMap[itemA+"-"+itemC]
				_, exists1 := lineMap[itemB+"-"+itemC]
				exists = exists0 && exists1
			}
			if exists {
				itemSet := make(map[string]bool)
				itemSet[itemA] = true
				itemSet[itemB] = true
				itemSet[itemC] = true
				itemSet[itemD] = true

				if len(itemSet) == 3 {
					keys := slices.Collect(maps.Keys(itemSet))
					sort.Strings(keys)

					startsWithT := false
					for _, item := range keys {
						if item[0] == 't' {
							startsWithT = true
							break
						}
					}

					if startsWithT {
						keyString := strings.Join(keys, "-")
						result[keyString] = true

					}

				}
			}

		}

	}

	fmt.Println(result)
	fmt.Println(len(result))
}

func part2() {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	lines := strings.Split(inputStr, "\n")

	lineMap := make(map[string]bool)
	itemCounter := make(map[string]bool)

	for _, line := range lines {
		items := strings.Split(line, "-")

		lineMap[line] = true
		lineMap[items[1]+"-"+items[0]] = true

		itemCounter[items[0]] = true
		itemCounter[items[1]] = true
	}

	pools := make(map[string][]string)

	for item := range itemCounter {
		for _, line := range lines {
			items := strings.Split(line, "-")

			itemA := items[0]
			itemB := items[1]

			var currentItem string
			var otherItem string

			if itemA == item {
				currentItem = itemA
				otherItem = itemB
			} else if itemB == item {
				currentItem = itemB
				otherItem = itemA
			}

			if currentItem != "" {
				_, exists := pools[item]
				if !exists {
					pools[item] = []string{}
				}

				otherConnections := true
				for _, anotherItem := range pools[item] {
					_, existsAnother := lineMap[otherItem+"-"+anotherItem]
					if !existsAnother {
						otherConnections = false
						break
					}
				}

				if otherConnections {
					pools[item] = append(pools[item], otherItem)

				}
			}

		}
	}

	// go through each item
	// loop through each other item
	// if has connection to everyone in current pool, add to current pool

	// do for everyone

	poolSet := make(map[string]int)

	for key, items := range pools {
		newKeys := []string{key}
		newKeys = append(newKeys, items...)
		slices.Sort(newKeys)
		comboKey := strings.Join(newKeys, ",")
		poolSet[comboKey] = len(newKeys)
	}

	//fmt.Println(poolSet)

	index := ""
	max := 0

	for key, count := range poolSet {
		if count > max {
			index = key
			max = count
		}
	}
	fmt.Println(index)
}

func main() {
	//part1()
	part2()
}
