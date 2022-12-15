import math
from typing import Union
from astar import Astar

input = ""

with open("input.txt") as input_file:
    input = input_file.read()


class Node:
    def __init__(self, value, data=None):
        self.value = value
        self.neighbor_indices = []
        self.neighbors = [],
        self.data = data

    def __repr__(self):
        return f"Node: {self.value} {self.data}"


class Graph:
    def __init__(self):
        self.nodes = []
        self.start_index = 0
        self.goal_index = 0
        self.start = None
        self.goal = None


graph = Graph()

input_lines = input.split("\n")
rows = len(input_lines)
cols = len(input_lines[0].strip())
for row, line in enumerate(input_lines):
    for col, char in enumerate(line):
        value = ord(char) - 97
        if char == "S":
            value = 0
            graph.start_index = row*cols + col

        elif char == "E":
            value = 25
            graph.goal_index = row*cols + col
        node = Node(value, (row, col))
        graph.nodes.append(node)

        top_row = row-1
        if row > 0:
            node.neighbor_indices.append(((row-1) * cols + col))

        if row < (rows - 1):
            node.neighbor_indices.append(((row + 1) * cols + col))

        if col > 0:
            node.neighbor_indices.append((row * cols + col - 1))

        if col < (cols - 1):
            node.neighbor_indices.append((row * cols + col + 1))

graph.start = graph.nodes[graph.start_index]
graph.goal = graph.nodes[graph.goal_index]

for node in graph.nodes:
    node.neighbors = [graph.nodes[i] for i in node.neighbor_indices if
                      graph.nodes[i].value - node.value < 2]

pathfinder = Astar(graph.nodes, graph.start, graph.goal, lambda node: 1 -
                   node.value / 24)


path = pathfinder.run()
print("steps", len(path) - 1)

zero_nodes = [node for node in graph.nodes if node.value == 0]


lengths = [len(Astar(graph.nodes, node, graph.goal, lambda node: node.value / 24).run())
           for node in zero_nodes]

lengths = [item - 1 for item in lengths if item != 0]
lengths.sort()
print(lengths[0])
