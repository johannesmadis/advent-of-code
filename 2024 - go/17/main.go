package main

import (
	"fmt"
	"slices"
)

func getOpValue(operand int, rA int, rB int, rC int) int {

	switch operand {
	case 0:
		return 0
	case 1:
		return 1
	case 2:
		return 2
	case 3:
		return 3
	case 4:
		return rA
	case 5:
		return rB
	case 6:
		return rC
	}
	return 0

}

func IntPow(n, m int) int {
	if m == 0 {
		return 1
	}

	if m == 1 {
		return n
	}

	result := n
	for i := 2; i <= m; i++ {
		result *= n
	}
	return result
}

func runProgram(initA int) [16]int {
	//registry := reg{initA, 0, 0}
	//program := []string{"0", "3", "5", "4", "3", "0"}
	rA := initA
	rB := 0
	rC := 0
	program := [16]int{2, 4, 1, 2, 7, 5, 1, 3, 4, 3, 5, 5, 0, 3, 3, 0} // strings.Split("2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0", ",")

	/*
		0 0 0 ^ 0 1 0 = 0 1 0	2
		0 0 1 ^ 0 1 0 = 0 1 1	3
		0 1 0 ^ 0 1 0 = 0 0 0	0
		0 1 1 ^ 0 1 0 = 0 0 1	1
		1 0 0 ^ 0 1 0 = 1 1 0	6
		1 0 1 ^ 0 1 0 = 1 1 1	7
		1 1 0 ^ 0 1 0 = 1 0 0	4
		1 1 1 ^ 0 1 0 = 1 0 1	5



		2 4: B = A % 8
		1 2: B = B ^ 2
		7 5: C = A / pow 2 B
		1 3: B = B ^ 3 10
		4 3: B = B ^ C
		5 5: out B % 8
		0 3: A = A // 8
		3 0: loop back


		2412751343550330




	*/
	pointer := 0
	result := [16]int{}
	rI := 0
	for len(program) > pointer {
		comboOperand := getOpValue(program[pointer+1], rA, rB, rC)
		litOperand := program[pointer+1]

		jump := 2
		switch program[pointer] {
		case 0: // adv divide A by 2^operand
			rA = rA >> comboOperand
			break
		case 1: // bxl XOR of of B and lit

			rB = rB ^ litOperand
			break
		case 2:

			rB = comboOperand % 8
			break
		case 3:

			if rA == 0 {
				break
			}
			jump = litOperand - pointer
			break
		case 4:

			rB = rB ^ rC
			break

		case 5: // out

			result[rI] = comboOperand % 8
			rI++
			break

		case 6: // bdv divide A by 2^operand

			rB = rA >> comboOperand
			break

		case 7: // cdv divide A by 2^operand

			rC = rA >> comboOperand
			break

		}
		//fmt.Println(registry, pointer)

		//bufio.NewReader(os.Stdin).ReadBytes('\n')

		pointer += jump
	}

	return result
}

func part1() {
	fmt.Println(runProgram(37221334433268))
}
func part2() {
	//intended_result := "[2,4,1,2,7,5,1,3,4,3,5,5,0,3,3,0]"
	//fmt.Println(runProgram((8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 1) * (8 + 2) * (8 + 0) * (8 + 0) * (8 + 0)))

	intended_result := []int{2, 4, 1, 2, 7, 5, 1, 3, 4, 3, 5, 5, 0, 3, 3, 0}
	//value := 0b0000000000000000

	candidates := make(map[int]bool)
	candidates[0] = true

	finalResults := []int{}

	for resultIndex := 15; resultIndex >= 0; resultIndex-- {
		fmt.Println(resultIndex)
		next_candidates := make(map[int]bool)
		for a := 0; a < 8; a++ {
			fmt.Printf("Try %b for candidates\n", a)

			for candidate := range candidates {
				testValue := candidate + a
				//fmt.Printf("Testvalue %d to get %d \n", testValue, intended_result[resultIndex])
				//fmt.Println(runProgram(testValue))

				if runProgram(testValue)[0] == intended_result[resultIndex] {
					if resultIndex == 0 {
						finalResults = append(finalResults, testValue)
					}

					next := testValue << 3

					next_candidates[next] = true

				}

			}
		}
		candidates = next_candidates

	}

	slices.Sort(finalResults)
	fmt.Println(finalResults)

}

func main() {
	part1()
	//part2()
}
