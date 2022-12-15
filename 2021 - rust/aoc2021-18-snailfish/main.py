from __future__ import annotations
from typing import Union
from math import floor, ceil


class pair:
    def __init__(self, a: int | pair, b: int | pair):
        self.left = a
        self.right = b
        self.parent: Union[None, pair] = None
        self.is_left: bool = True

        if isinstance(self.left, pair):
            self.left.parent = self

        if isinstance(self.right, pair):
            self.right.parent = self

    def can_explode(self):
        return self.parent != None and self.parent.parent != None and self.parent.parent.parent != None and self.parent.parent.parent.parent != None

    def can_split(self):
        return (isinstance(self.right, int) and self.right >= 10) or isinstance(self.left, int) and self.left >= 10

    def explode(self):
        print("explode")
        if self.parent != None:
            self.parent.add_left(self.left)
            self.parent.add_right(self.right)

            if self.is_left:
                self.parent.left = 0
            else:
                self.parent.right = 0

    def add_right(self, value):
        if isinstance(self.right, int):
            self.right += value
        elif self.parent != None:
            self.parent.add_right(value)

    def add_left(self, value):
        if isinstance(self.left, int):
            self.left += value
        elif self.parent != None:
            self.parent.add_left(value)

    def split(self):
        if isinstance(self.left, int) and self.left >= 10:
            self.left = pair(floor(self.left / 2), ceil(self.left/2))

        if isinstance(self.right, int) and self.right >= 10:
            self.right = pair(floor(self.right / 2), ceil(self.right/2))

    def reduce(self, level=0):
        print("reduce", level, self)
        if isinstance(self.right, pair):
            print("reduce left")
            self.right.reduce(level + 1)

        if isinstance(self.left, pair):
            print("reduce right")
            self.left.reduce(level + 1)

        if self.can_explode():
            print("can explode")
            self.explode()
            self.parent.reduce(level + 1)

        if self.can_split():
            self.split()
            self.reduce(level + 1)

    def get_magnitude(self):
        pass

    def __str__(self):
        return "[" + str(self.left) + ", " + str(self.right) + "]"

    # static

    def add(a: Union[int, pair], b: Union[int, pair]) -> pair:
        result = pair(a, b)
        a.is_left = True
        b.is_left = False

        result.reduce()

        return result


# parse input into pairs
def parse_input(lists):
    a, b = lists[0], lists[1]
    if isinstance(a, list):
        a = parse_input(a)

    if isinstance(b, list):
        b = parse_input(b)

    return pair(a, b)


input = """[1,1]
[2,2]
[3,3]
[4,4]
[5,5]"""

lines = input.split("\n")
result = parse_input(eval(lines[0]))

for line_number in range(1, len(lines)):
    line = parse_input(eval(lines[line_number]))
    result = result.add(line)

print(result)
print(result.get_magnitude())
