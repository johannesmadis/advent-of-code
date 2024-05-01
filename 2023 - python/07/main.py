import re
import math


def parse_input():
    lines = []
    with open("./input.txt") as input_file:
        lines = input_file.readlines()
        lines = [line.strip() for line in lines]

    instructions = lines[0]
    instructions = instructions.replace("L", "0").replace("R", "1")
    instructions = [int(char) for char in instructions]

    items = lines[2:]

    map = {}

    for item in items:
        matches = re.match(r"(.+) = \((.+), (.+)\)", item)
        id, child0, child1 = matches.groups()

        map[id] = (child0, child1, id)
    return instructions, map


def part1(origin="AAA", end="ZZZ"):
    instructions, map = parse_input()

    start = map[origin]
    current = start
    index = 0
    while current != map[end]:
        instruction = instructions[index % len(instructions)]
        current = map[current[instruction]]
        index += 1

    return index


def check_currents(currents):
    for key in currents:
        if key[0][2] != "Z":
            return False
    return True


def part2():
    instructions, map = parse_input()

    starts = [map[item] for item in map if item[2] == "A"]
    ends = [map[item] for item in map if item[2] == "Z"]

    indices = []
    for start in starts:
        index = 0
        current = start
        while current[2][2] != "Z":
            instruction = instructions[index % len(instructions)]
            current = map[current[instruction]]
            index += 1

        indices.append(index)

    print(math.lcm(*indices))


# print(part1())
part2()
