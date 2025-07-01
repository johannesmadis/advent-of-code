package main

import (
	"container/heap"
	"fmt"
	"os"
	"strings"
)

//

// An Item is something we manage in a priority queue.
type Item struct {
	value    node // The value of the item; arbitrary.
	priority int  // The priority of the item in the queue.
	// The index is needed by update and is maintained by the heap.Interface methods.
	index int // The index of the item in the heap.
}

// A PriorityQueue implements heap.Interface and holds Items.
type PriorityQueue []*Item

func (pq PriorityQueue) Len() int { return len(pq) }

func (pq PriorityQueue) Less(i, j int) bool {
	// We want Pop to give us the highest, not lowest, priority so we use greater than here.
	return pq[i].priority > pq[j].priority
}

func (pq PriorityQueue) Swap(i, j int) {
	pq[i], pq[j] = pq[j], pq[i]
	pq[i].index = i
	pq[j].index = j
}

func (pq *PriorityQueue) Push(x any) {
	n := len(*pq)
	item := x.(*Item)
	item.index = n
	*pq = append(*pq, item)
}

func (pq *PriorityQueue) Pop() any {
	old := *pq
	n := len(old)
	item := old[n-1]
	old[n-1] = nil  // don't stop the GC from reclaiming the item eventually
	item.index = -1 // for safety
	*pq = old[0 : n-1]
	return item
}

// update modifies the priority and value of an Item in the queue.
func (pq *PriorityQueue) update(item *Item, value node, priority int) {
	item.value = value
	item.priority = priority
	heap.Fix(pq, item.index)
}

type vec2 struct {
	x int
	y int
}

type node struct {
	pos    vec2
	parent *node
}

func getNeighbors(fields [][]string, pos vec2) []vec2 {

	neighbors := []vec2{}
	w := len(fields[0])
	h := len(fields)

	if pos.x > 0 && fields[pos.y][pos.x-1] != "#" {
		neighbors = append(neighbors, vec2{pos.x - 1, pos.y})
	}
	if pos.x < (w-1) && fields[pos.y][pos.x+1] != "#" {
		neighbors = append(neighbors, vec2{pos.x + 1, pos.y})
	}
	if pos.y > 0 && fields[pos.y-1][pos.x] != "#" {
		neighbors = append(neighbors, vec2{pos.x, pos.y - 1})
	}
	if pos.y < (h-1) && fields[pos.y+1][pos.x] != "#" {
		neighbors = append(neighbors, vec2{pos.x, pos.y + 1})
	}

	return neighbors
}

func dijkstra(fields [][]string, sX int, sY int) node {

	closed := make(map[vec2]bool)

	queue := PriorityQueue{}

	startNode := node{vec2{sX, sY}, nil}
	startItem := Item{}
	startItem.value = startNode

	heap.Init(&queue)
	heap.Push(&queue, &startItem)
	for queue.Len() > 0 {
		currentNode := heap.Pop(&queue).(*Item)
		cVec := currentNode.value.pos
		closed[cVec] = true

		neighbors := getNeighbors(fields, cVec)

		for _, neighbor := range neighbors {
			neighborNode := node{neighbor, &currentNode.value}

			if fields[neighbor.y][neighbor.x] == "E" {
				return neighborNode
			}
			_, exists := closed[neighbor]
			if !exists {
				neighborNode := node{neighbor, &currentNode.value}
				item := Item{}
				item.value = neighborNode

				heap.Push(&queue, &item)
			}
		}

	}
	return node{}
}

func cloneFields(original [][]string) [][]string {

	fields := [][]string{}
	for _, line := range original {
		newLine := []string{}
		for _, char := range line {
			newLine = append(newLine, char)
		}
		fields = append(fields, newLine)
	}
	return fields
}

func getHistory(item node) []vec2 {

	history := []vec2{}
	currentItem := item
	for currentItem.parent != nil {
		history = append(history, (*currentItem.parent).pos)
		currentItem = *currentItem.parent
	}
	return history
}

func part1() {

	input, _ := os.ReadFile("./input.txt")
	inputLines := strings.Split(string(input), "\n")

	fields := [][]string{}

	startX, startY := 0, 0

	for y, line := range inputLines {
		row := []string{}
		for x, char := range strings.Split(line, "") {
			row = append(row, char)
			if char == "S" {
				startX = x
				startY = y
			}

		}
		fields = append(fields, row)
	}

	item := dijkstra(fields, startX, startY)
	history := getHistory(item)

	regularCost := len(history)

	// create map for each possible cheat and solve it
	maps := make(map[vec2][][]string)
	for x := 0; x < len(fields[0]); x++ {
		for y := 0; y < len(fields); y++ {
			val := fields[y][x]
			if val == "#" {
				newFields := cloneFields(fields)
				newFields[y][x] = "."
				maps[vec2{x, y}] = newFields
			}
		}
	}

	sum := 0
	for _, altFields := range maps {
		targetItem := dijkstra(altFields, startX, startY)
		altHistory := getHistory(targetItem)
		altHistoryCost := len(altHistory)
		if regularCost-altHistoryCost >= 100 {
			sum++
		}

	}

	fmt.Println(sum)

}
func main() {
	//part1()
}
