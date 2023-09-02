from __future__ import annotations
import math
from queue import PriorityQueue
from typing import List, Dict


class Node:
    def __init__(self, name: str):
        self.name = name
        self.neighbors = []
        self.distances = {}
        self.value = None

    def __repr__(self):
        return f"Node({self.name})"


class Edge:
    def __init__(self, a: str, b: str, w: int):
        self.a = a
        self.b = b
        self.w = w

    def __repr__(self):
        return f"Edge({self.a} - {self.b}; {self.w})"


class Graph:
    def __init__(self, nodes: List[Node], edges: List[Edge]):
        self.nodes = {}
        for node in nodes:
            self.nodes[node.name] = node
        self.edges = edges

    def __repr__(self):
        return f"Graph( nodes: {self.nodes}; edges: {self.edges})"

    def dijkstra(self, start_node: Node):
        distances: Dict[str] = {}

        distances[start_node.name] = 0

        for node_name in self.nodes:
            node = self.nodes[node_name]
            distances[node.name] = math.inf

        queue = PriorityQueue()
        queue.put((0, start_node.name))

        while not queue.empty():
            current_distance, current_node_name = queue.get()
            current_node = self.nodes[current_node_name]
            if current_distance > distances[current_node.name]:
                continue

            for neighbor, weight in self.nodes[current_node.name].neighbors:
                distance = current_distance + weight

                if distance < distances[neighbor]:
                    distances[neighbor] = distance
                    current_node
                    queue.put((distance, neighbor))

        return distances

    def calculate_distances(self):
        for edge in self.edges:
            start_node, end_node = self.nodes[edge.a], self.nodes[edge.b]
            start_node.neighbors.append((edge.b, edge.w))
            end_node.neighbors.append((edge.a, edge.w))

        all_distances = {}
        for node_name in self.nodes:
            all_distances[node_name] = self.dijkstra(self.nodes[node_name])

        return all_distances
