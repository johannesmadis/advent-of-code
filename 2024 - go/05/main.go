package main

import (
	"fmt"
	"os"
	"sort"
	"strconv"
	"strings"
)

type Node struct {
	id       int
	level    int
	children []int
	isRoot   bool
}

func readInput() ([]string, []string) {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	parts := strings.Split(inputStr, "\n\n")
	graphList := strings.Split(parts[0], "\n")
	testList := strings.Split(parts[1], "\n")

	return graphList, testList
}

func makeNodes(graphList []string) map[int]Node {

	nodes := make(map[int]Node)

	for _, item := range graphList {
		items := strings.Split(item, "|")
		before, _ := strconv.Atoi(items[0])
		after, _ := strconv.Atoi(items[1])

		// check if exists
		_, existsBefore := nodes[before]
		if !existsBefore {
			nodes[before] = Node{before, 0, []int{}, true}

		}

		_, existsAfter := nodes[after]
		if !existsAfter {
			nodes[after] = Node{after, 0, []int{}, false}
		}

		nodeBefore := nodes[before]
		nodeAfter := nodes[after]

		nodeBefore.children = append(nodeBefore.children, after)
		nodeAfter.isRoot = false

		nodes[before] = nodeBefore
		nodes[after] = nodeAfter

	}

	return nodes

}

func findRoot(items map[int]Node) int {

	for _, item := range items {
		if item.isRoot {
			return item.id
		}
	}
	return 0
}

func assignNodeLevels(nodes map[int]Node, currentNodeId int, currentLevel int) {
	currentNode := nodes[currentNodeId]
	if currentLevel > currentNode.level {
		currentNode.level = currentLevel
	}
	nodes[currentNodeId] = currentNode

	for _, childId := range currentNode.children {
		assignNodeLevels(nodes, childId, currentLevel+1)
	}

}

func getStrFromSliceOfNodes(nodes []Node) string {

	result := []string{}
	for _, node := range nodes {
		result = append(result, strconv.Itoa(node.id))
	}

	return strings.Join(result, ",")
}

func main2() {
	// create a graph from nodes - edges
	// calculate levels
	// start at node which has no parents
	// each child will get level +1,
	// overwrite child level if larger than before
	graphList, testList := readInput()
	nodes := makeNodes(graphList)
	rootNodeId := findRoot(nodes)

	assignNodeLevels(nodes, rootNodeId, 0)

	//
	// analyse each row
	// sort according to levels
	// if sorted line is same as current line, add middle to sum

	sum := 0

	for _, line := range testList {
		lineItems := strings.Split(line, ",")
		middleItem, _ := strconv.Atoi(lineItems[len(lineItems)/2])

		// make a list of ints. Ints are node ids
		lineNodes := []Node{}
		for _, chars := range lineItems {
			parsedInt, _ := strconv.Atoi(chars)
			lineNodes = append(lineNodes, nodes[parsedInt])
		}

		// sort it based on node levels
		sort.Slice(lineNodes, func(i, j int) bool {
			return (lineNodes[i].level - lineNodes[j].level) < 0
		})

		if line == getStrFromSliceOfNodes(lineNodes) {
			fmt.Println(line, middleItem)
			sum += middleItem
		}

	}
	println(sum)

}

func testCorrectness(graphSet map[string]bool, items []string) bool {

	for index, item := range items {
		previousItems := items[:index]
		nextItems := items[index+1:]

		for _, previousItem := range previousItems {
			falsyPrevious := item + "|" + previousItem
			_, exists := graphSet[falsyPrevious]
			if exists {
				return false
			}
		}
		for _, nextItem := range nextItems {
			falsyNext := nextItem + "|" + item
			_, exists := graphSet[falsyNext]
			if exists {
				return false
			}
		}

	}
	return true
}

func part1() {
	graphList, testList := readInput()

	graphSet := make(map[string]bool)

	for _, item := range graphList {
		graphSet[item] = true
	}

	sum := 0

	for _, line := range testList {
		items := strings.Split(line, ",")
		correctlyOrdered := testCorrectness(graphSet, items)

		if correctlyOrdered {
			middleItem := items[len(items)/2]
			middleItemValue, _ := strconv.Atoi(middleItem)
			sum += middleItemValue
		}
	}

	fmt.Println(sum)
}

func part2() {
	graphList, testList := readInput()

	graphSet := make(map[string]bool)

	for _, item := range graphList {
		graphSet[item] = true
	}

	filteredTestList := []string{}

	for _, line := range testList {
		items := strings.Split(line, ",")
		correctlyOrdered := testCorrectness(graphSet, items)

		if !correctlyOrdered {
			filteredTestList = append(filteredTestList, line)
		}
	}

	sum := 0
	for _, line := range filteredTestList {
		items := strings.Split(line, ",")
		sort.Slice(items, func(i, j int) bool {
			beforeRule := items[i] + "|" + items[j] // current should be ahead
			afterRule := items[j] + "|" + items[i]  // current should be after
			_, beforeRuleExists := graphSet[beforeRule]
			_, afterRuleExists := graphSet[afterRule]

			return beforeRuleExists || !afterRuleExists
		})

		fmt.Println(items)

		middleItem := items[len(items)/2]
		middleItemValue, _ := strconv.Atoi(middleItem)
		sum += middleItemValue

	}
	fmt.Println(sum)

}

func main() {
	part1()
	part2()
}
