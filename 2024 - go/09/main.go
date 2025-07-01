package main

import (
	"fmt"
	"os"
	"slices"
	"strconv"
	"strings"
)

func repeatedSlice(value, n int) []int {
	arr := make([]int, n)
	for i := 0; i < n; i++ {
		arr[i] = value
	}
	return arr
}

func decompress(registry []int) []int {
	result := []int{}
	for index, length := range registry {
		var id int
		if index%2 == 0 {
			id = index / 2

		} else {
			id = -1
		}
		result = append(result, repeatedSlice(id, length)...)
	}
	return result
}

func defragment(filesystem []int) []int {
	result := []int{}
	// loop through original filesystem to find empty spaces
	// loop reverse through original filesystem to find next items to put to empty spaces
	// keep track of last index that has been moved, break loop if we would move something with smaller index than current empty space

	reverse_tracker := len(filesystem)

	itemCount := 0
	for _, item := range filesystem {
		if item != -1 {
			itemCount += 1
		}
	}

	for index, item := range filesystem {
		if index == itemCount {
			break
		}
		if item != -1 {
			result = append(result, item)
		} else {

			reverse_tracker -= 1

			for i := reverse_tracker; filesystem[reverse_tracker] == -1; i = i - 1 {
				reverse_tracker = i
			}
			result = append(result, filesystem[reverse_tracker])

		}
	}

	return result
}

func calculate_checksum(filesystem []int) int {
	sum := 0
	for index, id := range filesystem {
		if id == -1 {
			continue
		}
		sum += index * id
	}
	return sum
}

func part1() {
	input, _ := os.ReadFile("./input.txt")
	input_str := string(input)

	registry := []int{}

	for _, item := range strings.Split(input_str, "") {
		num, _ := strconv.Atoi(item)
		registry = append(registry, num)
	}

	filesystem := decompress(registry)

	defragmented := defragment(filesystem)

	checksum := calculate_checksum(defragmented)

	fmt.Println(checksum)
}

func decompress2(registry []int) [][]int {
	result := [][]int{}

	for index, length := range registry {
		var id int
		if index%2 == 0 {
			id = index / 2

		} else {
			id = -1
		}
		result = append(result, []int{id, length})
	}
	return result

}

func defragment2(filesystem [][]int) [][]int {
	for index := len(filesystem) - 1; index >= 0; index -= 2 {

		item := filesystem[index]
		length := item[1]
		// loop through filesystem to find empty space with enough space
		// if found
		// change it to 0, insert current item into place, insert remainder empty space, remove from end together with end empty space, reincrease index,
		targetIndex := slices.IndexFunc(filesystem, func(target []int) bool { return target[0] == -1 && target[1] >= length })

		if targetIndex != -1 && targetIndex < index {
			emptySpaceLength := filesystem[targetIndex][1]
			filesystem[targetIndex][1] = 0

			spaceAfter := -1
			spaceAfterIndex := index + 1
			if spaceAfterIndex < len(filesystem) {
				spaceAfter = filesystem[spaceAfterIndex][1]
			}

			// set space before moved item to length of moved item and space after it
			// delete moved item and space after it (if within bounds)

			if spaceAfter != -1 {
				filesystem = slices.Delete(filesystem, index, index+2) // remove both item and space after it
				filesystem[index-1][1] += item[1] + spaceAfter

			} else {
				filesystem = slices.Delete(filesystem, index, index+1) // remove only item
				filesystem[index-1][1] += item[1]

			}

			filesystem = slices.Insert(filesystem, targetIndex+1, item)
			filesystem = slices.Insert(filesystem, targetIndex+2, []int{-1, emptySpaceLength - item[1]})

			index += 2
		}

	}

	return filesystem
}

func checksum2(filesystem [][]int) int {
	sum := 0

	counter := 0
	for _, item := range filesystem {

		if item[0] != -1 {
			for i := counter; i < counter+item[1]; i++ {
				sum += i * item[0]
			}
		}
		counter += item[1]
	}
	return sum

}

func part2() {
	input, _ := os.ReadFile("./input.txt")
	input_str := string(input)

	registry := []int{}

	for _, item := range strings.Split(input_str, "") {
		num, _ := strconv.Atoi(item)
		registry = append(registry, num)
	}

	filesystem := decompress(registry)
	decompressed := decompress2(registry)

	i := len(filesystem)
	counter := len(decompressed) - 1

	for true {

		item := decompressed[counter]
		currentIndex := i - item[1]

		if counter > 0 {
			i = i - item[1] - decompressed[counter-1][1]
		}

		// find index where to put n amount of item

		insertIndex := -1
		for index := 0; index < len(filesystem)-item[1]; index += 1 {
			emptyCounter := 0
			for subindex := 0; subindex < item[1]; subindex++ {
				if filesystem[subindex+index] == -1 {
					emptyCounter++
				}
				if emptyCounter == item[1] {
					insertIndex = index
					break
				}

			}
			if insertIndex != -1 {
				break
			}
		}

		if insertIndex != -1 && insertIndex < currentIndex {
			// set current item to zeroes

			for n := currentIndex; n < currentIndex+item[1]; n++ {
				filesystem[n] = -1
			}
			// set items at insertIndex to current values
			for n := insertIndex; n < insertIndex+item[1]; n++ {
				filesystem[n] = item[0]
			}

		}

		counter -= 2

		if counter == -2 {
			break
		}
	}

	//filesystem = defragment2(filesystem)

	//checksum := checksum2(filesystem)

	fmt.Println(calculate_checksum(filesystem))

}

func main() {

	//part1()
	part2()
}
