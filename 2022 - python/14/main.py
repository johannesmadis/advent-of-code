from __future__ import annotations
from typing import Tuple, List
import math
import time
input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""

with open("input.txt") as file_input:
    input = file_input.read()


class Point:
    def __init__(self, x: int, y: int):
        self.x = int(x)
        self.y = int(y)

    def clone(self):
        return Point(self.x, self.y)

    def __add__(self, other: Point):
        return Point(self.x + other.x, self.y + other.y)

    def __repr__(self):
        return f"Point[{self.x},{self.y}]"

    def __hash__(self):
        return hash((self.x, self.y))

    def __eq__(self, other: Point):
        return self.x == other.x and self.y == other.y


class Bounds:
    def __init__(self):
        self.min_x = math.inf
        self.min_y = math.inf
        self.max_x = -math.inf
        self.max_y = -math.inf

    def add_point(self, other: Point):
        if other.x < self.min_x:
            self.min_x = other.x
        if other.x > self.max_x:
            self.max_x = other.x
        if other.y < self.min_y:
            self.min_y = other.y
        if other.y > self.max_y:
            self.max_y = other.y

    def union(self, other: Bounds):
        self.min_x = self.min_x if self.min_x < other.min_x else other.min_x
        self.min_y = self.min_y if self.min_y < other.min_y else other.min_y
        self.max_x = self.max_x if self.max_x > other.max_x else other.max_x
        self.max_y = self.max_y if self.max_y > other.max_y else other.max_y

    def __repr__(self):
        return f"Bounds: x[{self.min_x},{self.max_x}], y[{self.min_y},{self.max_y}]"


class Polyline:
    def __init__(self, corners: List[Point]):

        self.corners = corners
        self.points: List[Point] = []

        for i in range(len(corners)-1):
            start = corners[i]
            end = corners[i+1]

            step_x = 1 if start.x < end.x else -1
            for x in range(start.x, end.x, step_x):
                self.points.append(Point(x, end.y))

            step_y = 1 if start.y < end.y else -1
            for y in range(start.y, end.y, step_y):
                self.points.append(Point(start.x, y))
        self.points.append(self.corners[-1])

    def get_bounds(self) -> Tuple[complex, complex]:
        x, y = zip(*[(point.x, point.y) for point in self.points])

        bounds = Bounds()
        for point in self.points:
            bounds.add_point(point)

        return bounds

    def __repr__(self):
        return f"Polyline {self.points}"


polylines = []

for line in input.split("\n"):
    points_str = [point.split(",") for point in line.split(" -> ")]
    points = [Point(x, y) for [x, y] in points_str]
    polylines.append(Polyline(points))


SAND_ORIGIN = Point(500, 0)


class Map:

    def __init__(self, polylines: List[Polyline]):
        self.polylines = polylines

        self.bounds = Bounds()
        bounds_list = [polyline.get_bounds() for polyline in polylines]

        for b in bounds_list:
            self.bounds.union(b)

        self.points = set()
        for polyline in self.polylines:
            for point in polyline.points:
                self.points.add(point)
        self.sand = []

    def check_end_condition(self, location: Point):
        # if any of sand is less than min or more than max x or more than max_y
        return location.y > self.bounds.max_y

    def step(self, condition):

        stuck = False

        sand_piece = Point(SAND_ORIGIN.x, SAND_ORIGIN.y)
        result = sand_piece.clone()
        end = condition(sand_piece)

        while (not stuck) and (not end):
            end = condition(sand_piece)
            if end:
                break

            sand_piece += Point(0, 1)
            if sand_piece not in self.points:
                result = sand_piece.clone()
                continue

            sand_piece += Point(-1, 0)

            if sand_piece not in self.points:
                result = sand_piece.clone()
                continue

            sand_piece += Point(2, 0)
            if sand_piece not in self.points:
                result = sand_piece.clone()
                continue

            stuck = True
            break

        if stuck:
            self.points.add(result)
            self.sand.append(result)
            return True

        return False

    def run(self):
        running = True
        while running:
            running = self.step(condition=self.check_end_condition)
            # time.sleep(1)

    def step2(self):

        current = Point(500, 0)

        while True:
            next = (current + Point(0, 1), current +
                    Point(-1, 1), current + Point(1, 1))
            next_available = False
            for potential_next in next:
                if potential_next not in self.points and potential_next.y <= (self.bounds.max_y + 1):
                    current = potential_next
                    next_available = True
                    break

            if next_available:
                continue

            # didnt find any next which isnt in points
            # means that current should be recorded
            self.points.add(current)
            self.sand.append(current)
            break

        return current == Point(500, 0)

    def run2(self):
        while True:
            if self.step2():
                break


map = Map(polylines)


map.run()
print(len(map.sand))

map2 = Map(polylines)
map2.run2()

print(len(map2.sand), map2.bounds)
