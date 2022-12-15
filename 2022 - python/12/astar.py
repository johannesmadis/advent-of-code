from queue import PriorityQueue
from typing import Dict, Callable, Any
import math


# node must have .value field and .neighbors fields
# start and goals must be nodes within nodes array
# nodes must be array of nodes
# heuristic accepts node as argument and outputs a number

def _distance(current, neighbor):
    return 1


def _heuristic(neighbor):
    return neighbor.value


class Astar:

    def __init__(self, nodes, start, goal, heuristic=_heuristic, distance=_distance):
        self.nodes: nodes
        self.distance = distance

        self.heuristic = heuristic
        self.start = start
        self.goal = goal
        self.came_from = {}

        self.open_set = PriorityQueue()
        self.open_set_hash = {start: True}

        self.open_set.put_nowait((0, 0, start))
        self.queue_counter = 1

        self.g_score = {}
        self.g_score[start] = 0

        self.f_score = {}
        self.f_score[start] = self.heuristic(start)

    def reconstruct_path(self, current):
        total_path = [current]
        while current in self.came_from:
            current = self.came_from[current]
            total_path.append(current)

        total_path.reverse()

        return total_path

    def run(self):

        start, goal = self.start, self.goal

        while len(self.open_set_hash) != 0:
            current_fscore, index, current = self.open_set.get_nowait()
            del self.open_set_hash[current]

            if current == goal:
                return self.reconstruct_path(current)

            for neighbor in current.neighbors:

                # since up,down,left,right, no manhattan distance needed - next is always 1 step further
                # +1 is distance(current, neighbor)
                t_score = self.g_score[current] + \
                    self.distance(current, neighbor)

                self.g_score.setdefault(neighbor, math.inf)
                if t_score < self.g_score[neighbor]:
                    self.g_score[neighbor] = t_score

                    h = self.heuristic(neighbor)

                    self.f_score[neighbor] = t_score + h

                    self.came_from[neighbor] = current

                    if neighbor not in self.open_set_hash:
                        self.open_set.put_nowait(
                            (self.f_score[neighbor], self.queue_counter, neighbor))
                        self.queue_counter += 1
                        self.open_set_hash[neighbor] = True

        return []
