from __future__ import annotations
import sys

sys.setrecursionlimit(100000)


Directions = {"R": (1, 0), "D": (0, -1), "L": (-1, 0), "U": (0, 1)}


def setup(points):

    start = (0, 0)
    current = start

    map = {}

    max_x = max([point[0] for point in points]) + 1
    max_y = max([point[1] for point in points]) + 1
    min_x = min([point[0] for point in points]) - 1
    min_y = min([point[1] for point in points]) - 1

    delta_x = max_x - min_x + 1
    delta_y = max_y - min_y + 1

    map = []

    for y in range(min_y, max_y + 1):
        map.append([])
        for x in range(min_x, max_x + 1):
            map[-1].append(True if (x, y) in points else False)

    return map, delta_x, delta_y, points


# start at 0,0, get all neighbors
# if neighbor exists and not border and not in set, add to set
# repeat for all unique neighbors


def get_neighbors(pt, border_map):
    neighbors = [
        (pt[0] + Directions[dir][0], pt[1] + Directions[dir][1]) for dir in Directions
    ]
    neighbors = [
        neighbor
        for neighbor in neighbors
        if neighbor[0] >= 0
        and neighbor[0] < len(border_map[0])
        and neighbor[1] >= 0
        and neighbor[1] < len(border_map)
        and border_map[neighbor[1]][neighbor[0]] != True
    ]

    return neighbors


def fill_map(current, map):

    neighbors = get_neighbors(current, map)

    for neighbor in neighbors:
        map[neighbor[1]][neighbor[0]] = True
        fill_map(neighbor, map)


def part1():
    lines = []

    with open("./input.txt") as input_file:
        lines = [line.split() for line in input_file.readlines()]

    start = (0, 0)
    current = start
    points = set()
    points.add(start)

    for line in lines:
        dir, times, color = line
        times = int(times)

        for _ in range(times):
            current = (
                current[0] + Directions[dir][0],
                current[1] + Directions[dir][1],
            )
            points.add(current)

    map, delta_x, delta_y, points = setup(points)

    fill_map((0, 0), map)

    print(delta_x * delta_y - (sum([sum(line) for line in map]) - len(points)))


part1()
