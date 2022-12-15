from __future__ import annotations
from typing import List


class Cube:
    def __init__(self, x: int, y: int, z: int, w: int, active: bool = False):
        self.x = x
        self.y = y
        self.z = z
        self.w = w
        self.active = active
        self.pending = None
        self.neighbors = []

    def queue_update(self, value: bool) -> bool:
        self.pending = value
        return self.pending

    def update(self) -> bool:
        self.active = self.pending
        self.pending = None
        return self.active

    def set_neighbors(self, cubes):
        for z in range(self.z - 1, self.z + 2):
            if z in cubes:
                for y in range(self.y - 1, self.y + 2):
                    if y in cubes[z]:
                        for x in range(self.x - 1, self.x + 2):
                            if x in cubes[z][y]:
                                for w in range(self.w - 1, self.w + 2):
                                    if w in cubes[z][y][x]:
                                        neighbor = cubes[z][y][x][w]
                                        if self is not neighbor:
                                            self.neighbors.append(
                                                cubes[z][y][x][w])


class Conway:
    def __init__(self, max_range):
        # z level
        self.max = max_range
        self.cubes = {}
        self.list = []

        for x in range(-self.max, self.max + 6):
            for y in range(-self.max, self.max + 6):
                for z in range(-self.max, self.max):
                    for w in range(-self.max, self.max):
                        self.get(x, y, z, w)

        for cube in self.list:
            cube.set_neighbors(self.cubes)

    def get(self, x, y, z, w):
        # Z
        self.cubes.setdefault(z, {})
        # Y
        self.cubes[z].setdefault(y, {})
        # x
        self.cubes[z][y].setdefault(x, {})

        if w not in self.cubes[z][y][x]:
            cube = Cube(x, y, z, w, False)
            self.cubes[z][y][x][w] = cube
            self.list.append(cube)

        return self.cubes[z][y][x][w]

    def set(self, x, y, z, w, active):
        cube = self.get(x, y, z, w)
        cube.queue_update(active)
        cube.update()

    def next_round(self):
        for cube in self.list:
            neighbor_values = [int(neighbor.active)
                               for neighbor in cube.neighbors]
            active_neighbors = sum(neighbor_values)
            if cube.active:
                cube.queue_update(active_neighbors ==
                                  2 or active_neighbors == 3)
            else:
                cube.queue_update(active_neighbors == 3)

        # update
        for cube in self.list:
            cube.update()


conway = Conway(16)

for lineI, line in enumerate(open("17.input.txt").read().split("\n")):
    for charI, char in enumerate(line):
        conway.set(lineI, charI, 0, 0, char == "#")


for _ in range(6):
   # conway.print()
    conway.next_round()

print(sum([int(cube.active) for cube in conway.list]))
