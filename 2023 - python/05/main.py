from __future__ import annotations
import math
import re
from typing import List


def convert(input, ranges):
    for range_data in ranges:
        target, start, length = range_data
        if input > start and input < start + length:
            return target + input - start

    return input


data = ""


with open("input.txt") as input_file:
    data = input_file.read()

inputs = data.split("\n\n")

seeds = inputs[0]
input_seeds = [int(input) for input in re.findall(r"(\d+)", seeds)]

converters = inputs[1:]

converting_groups = []

for converter in converters:
    lines = [line.strip() for line in converter.split("\n")]
    lines = [[int(item) for item in line.split(" ")] for line in lines[1:]]
    converting_groups.append(lines)


result = []
for input_seed in input_seeds:
    current = input_seed
    for converting_group in converting_groups:
        current = convert(current, converting_group)

    result.append(current)

print(sorted(result))


# part 2


class Interval:
    def __init__(self, start: int, length: int):
        self.start = start
        self.length = length
        self.end = self.start + self.length

    def __contains__(self, element: int | Interval):
        if isinstance(element, int):
            return element >= self.start and element < self.end

        if isinstance(element, Interval):
            return element.start >= self.start and element.end <= self.end

        raise TypeError("Only ints and Intervals allowed")

    def split(self, splitter: int) -> List[Interval]:
        if splitter not in self:
            return [self]

        results: List[Interval] = []

        results.append(self.start, self.start - splitter)
        results.append(splitter, self.end - splitter)

        return results


class IntervalConverter:
    def __init__(self, source: Interval, target: Interval):
        self.source = source
        self.target = target


# Start interval
# splits to n intervals
# each split has a corresponding target interval
# each target interval splits to next level
# where each have target intervals
# continue for each level
# final list should have lots of smaller intervals which correspond to start
# record smallest start

# do that to all other starting intervals
# return smallest number

start = Interval(79, 14)

converters = {
    IntervalConverter(Interval(98, 2), Interval(50, 2)),
    IntervalConverter(Interval(50, 48), Interval(52, 48)),
}

for converter in converters:
