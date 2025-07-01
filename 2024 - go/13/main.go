package main

import (
	"fmt"
	"math"
	"os"
	"regexp"
	"strconv"
	"strings"
)

func part1() {
	input, _ := os.ReadFile("./input.txt")
	inputStr := string(input)

	r, _ := regexp.Compile(`\d+`)

	inputCases := strings.Split(inputStr, "\n\n")

	sum := 0.0

	for _, inputCase := range inputCases {
		data := strings.Split(inputCase, "\n")
		matches := r.FindAllString(data[0], -1)
		matches2 := r.FindAllString(data[1], -1)
		matches3 := r.FindAllString(data[2], -1)

		xA, _ := strconv.ParseFloat(matches[0], 64)
		yA, _ := strconv.ParseFloat(matches[1], 64)

		xB, _ := strconv.ParseFloat(matches2[0], 64)
		yB, _ := strconv.ParseFloat(matches2[1], 64)

		destX, _ := strconv.ParseFloat(matches3[0], 64)
		destY, _ := strconv.ParseFloat(matches3[1], 64)

		destX += 10000000000000
		destY += 10000000000000

		countB := (destX*yA - xA*destY) / (xB*yA - xA*yB)
		countA := (destX*yB - xB*destY) / (xA*yB - yA*xB)

		if math.Floor(countA) == countA && math.Floor(countB) == countB {
			sum += 3*countA + countB
		}

	}
	fmt.Println(int(sum))
}

func main() {
	part1()

	/*
			destX = countA * xA + countB * xB
			destY = countA * yA + countB * yB

			countB = (destY - countA * yA) / yB

			destX = countA * xA + xB * (destY - countA * yA) / yB
			destX = countA * xA + (xB * destY - countA * yA * xB) / yB

			destX * yB = countA * xA * yB + xB * destY - countA * yA * xB
			destX * yB - xB * destY = countA * (xA * yB - yA * xB)
			countA = (destX * yB - xB * destY) / (xA * yB - yA * xB)



			Button A: X+94, Y+34
		Button B: X+22, Y+67
		Prize: X=8400, Y=5400
	*/

}
