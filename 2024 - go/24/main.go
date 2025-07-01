package main

import (
	"fmt"
	"os"
	"slices"
	"sort"
	"strconv"
	"strings"
)

type gate struct {
	a        string
	b        string
	function string
	result   string
	checked  bool
}

type value struct {
	field string
	value bool
}

func boolToInt(b bool) int {
	if b {
		return 1
	}
	return 0
}

func gateFunc(gate gate, values map[string]bool) bool {
	switch gate.function {
	case "AND":
		return values[gate.a] && values[gate.b]
	case "OR":
		return values[gate.a] || values[gate.b]
	case "XOR":
		return values[gate.a] != values[gate.b]
	}
	return false

}

func part1() {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	inputParts := strings.Split(inputStr, "\n\n")

	initialValuesStr := strings.Split(inputParts[0], "\n")
	gatesStr := strings.Split(inputParts[1], "\n")

	values := make(map[string]bool)
	gates := []gate{}

	for _, line := range initialValuesStr {
		fields := strings.Fields(line)
		values[fields[0][:3]], _ = strconv.ParseBool(fields[1])
	}

	for _, line := range gatesStr {
		fields := strings.Fields(line)
		gates = append(gates, gate{fields[0], fields[2], fields[1], fields[4], false})
	}

	gateLength := len(gates)

	for gateLength > 0 {
		for gI, gate := range gates {
			if gate.checked {
				continue
			}
			_, existsA := values[gate.a]
			_, existsB := values[gate.b]
			if existsA && existsB {
				values[gate.result] = gateFunc(gate, values)
				gate.checked = true
				gates[gI] = gate
				gateLength--
			}

		}
	}
	//fmt.Println(gates)

	zValues := []value{}

	for key, val := range values {
		if key[0] == 'z' {
			zValues = append(zValues, value{key, val})
		}
	}

	sort.Slice(zValues, func(i int, j int) bool {
		return zValues[i].field > zValues[j].field
	})
	//fmt.Println(zValues)

	binStr := ""
	for _, bin := range zValues {
		binStr += strconv.Itoa(boolToInt(bin.value))
	}

	fmt.Println(strconv.ParseInt(binStr, 2, 64))

}

func part2() {
	// whats the intended result
	// x +y

	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	inputParts := strings.Split(inputStr, "\n\n")

	initialValuesStr := strings.Split(inputParts[0], "\n")
	gatesStr := strings.Split(inputParts[1], "\n")

	values := make(map[string]bool)
	gates := []gate{}

	for _, line := range initialValuesStr {
		fields := strings.Fields(line)
		values[fields[0][:3]], _ = strconv.ParseBool(fields[1])
	}

	for _, line := range gatesStr {
		fields := strings.Fields(line)
		gates = append(gates, gate{fields[0], fields[2], fields[1], fields[4], false})
	}

	graph := []string{}

	for _, gate := range gates {
		graph = append(graph, gate.a+"_"+gate.function+"_"+gate.b+" -> "+gate.result)
		graph = append(graph, gate.result+" [shape=Msquare]")
		for _, gate2 := range gates {
			if gate2.a == gate.result || gate2.b == gate.result {
				graph = append(graph, gate.result+" -> "+gate2.a+"_"+gate2.function+"_"+gate2.b)

			}
		}
	}
	for _, line := range graph {
		fmt.Println(line)
	}

	//graph := []string{}'

	exists, prevCarry := true, "rnv"

	for i := 1; i < 45; i++ {
		exists, prevCarry = patternExists(i, prevCarry, gates)
		fmt.Println(i, exists)
	}

	// x XOR y = xxory
	// c XOR xxory = z
	// c AND xxory = candxxory
	// x and b = xandb
	// candxxory or xandb = cout

	suspects := []string{"z11", "vkq", "z24", "mmk", "pvb", "qdq", "z38", "hqh"}
	slices.Sort(suspects)

	fmt.Println(strings.Join(suspects, ","))

}

func leftPad(a string) string {
	if len(a) < 2 {
		return "0" + a
	}
	return a
}

func patternExists(i int, prevCarry string, gates []gate) (bool, string) {
	xxoryI := slices.IndexFunc(gates, func(g gate) bool {
		return g.function == "XOR" && ((g.a == "x"+leftPad(strconv.Itoa(i))) && (g.b == "y"+leftPad(strconv.Itoa((i)))) || (g.b == "x"+leftPad(strconv.Itoa(i))) && (g.a == "y"+leftPad(strconv.Itoa((i)))))
	})

	if xxoryI == -1 {
		fmt.Println("no xxory")
		return false, ""
	}

	xxory := gates[xxoryI].result

	zI := slices.IndexFunc(gates, func(g gate) bool {
		return g.function == "XOR" && ((g.a == prevCarry && g.b == xxory) || (g.a == xxory && g.b == prevCarry))
	})
	if zI == -1 {
		fmt.Println("no zI", prevCarry, i, xxory)

		return false, ""
	}

	candI := slices.IndexFunc(gates, func(g gate) bool {
		return g.function == "AND" && ((g.a == prevCarry && g.b == xxory) || (g.a == xxory && g.b == prevCarry))
	})

	if candI == -1 {
		fmt.Println("no candI")

		return false, ""
	}

	candxxory := gates[candI].result

	xandbI := slices.IndexFunc(gates, func(g gate) bool {
		index := leftPad(strconv.Itoa(i))
		return g.function == "AND" &&
			((g.a == "x"+index && g.b == "y"+index) ||
				(g.a == "y"+index && g.b == "x"+index))
	})
	if xandbI == -1 {
		fmt.Println("no xandbI")

		return false, ""
	}

	xandb := gates[xandbI].result

	coutI := slices.IndexFunc(gates, func(g gate) bool {
		return g.function == "OR" && ((g.a == candxxory && g.b == xandb) || (g.a == xandb && g.b == candxxory))
	})

	if coutI == -1 {
		fmt.Println("no coutI")

		return false, ""
	}

	cout := gates[coutI].result

	return true, cout

}

func main() {
	part1()
	part2()

}
