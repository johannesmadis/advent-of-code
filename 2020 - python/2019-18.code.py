
import json


class Node():
    def __init__(self, value, row_index, col_index):
        self.row = row_index
        self.col = col_index
        self.value = item
        self.type = "wal" if value == "#" else "cor"
        self.top = None
        self.left = None
        self.bottom = None
        self.right = None

    def set_top(self, node=None):
        self.top = node

    def set_bottom(self, node=None):
        self.bottom = node

    def set_left(self, node=None):
        self.left = node

    def set_right(self, node=None):
        self.right = node


class Graph():
    def __init__(self):
        self.nodes = []
        self.grid = []
        self.row = 0
        self.col = 0

    def add(self, node):
        self.nodes.append(node)
        # add to grid

        if (len(self.grid) <= node.row):
            self.grid.append([])

        self.grid[node.row].append(node)
        # set top and left for current node
        if (node.col != 0):
            neighbor = self.grid[node.row][node.col - 1]

            node.set_left(neighbor)
            neighbor.set_right(node)
        if (node.row != 0):
            neighbor = self.grid[node.row - 1][node.col]

            node.set_top(neighbor)
            neighbor.set_bottom(node)

        if (node.value == "@"):
            self.row = node.row
            self.col = node.col

    def move(self, iterator=0):
        # try all directions for current node.
        # for each direction calculate the value
        # sort
        # go forward with best
        # value is calculated by distance to all remaining keys (precalculated for each key gradient map)
        # if locked door is encountered, value goes to inf
        pass


graph = Graph()
with open("2019-18.input.txt") as f:
    lines = f.read().split("\n")
    for row_index, line in enumerate(lines):
        for col_index, item in enumerate(line):
            graph.add(Node(item, row_index, col_index))


def dump(item):
    return json.dumps(item.__dict__, default=lambda i: "node")


print(dump(graph))
