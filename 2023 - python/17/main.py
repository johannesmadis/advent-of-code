from enum import IntEnum
from typing import Literal
from __future__ import annotations
from heapq import heappop, heappush


Rotation = Literal["CCW", "CW"]

def Position(GridPoint, Direction) -> GridPoint:
    


class GridPoint(tuple):
    pass


class Direction(IntEnum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

    @staticmethod
    def rotate(facing: Direction, towards: Rotation):
        offset = 1 if towards == "CW" else -1
        return Direction((facing.value + offset) % 4)

    @staticmethod
    def offset(facing: Direction) -> GridPoint:
        return _ROW_COL_OFFSETS[facing]


_ROW_COL_OFFSETS: dict[Direction, GridPoint] = {
    Direction.UP: (-1, 0),
    Direction.RIGHT: (0, 1),
    Direction.DOWN: (1, 0),
    Direction.LEFT: (0, -1),
}


State = tuple[int, Position, int]

class Solution():
    def part_1(self) -> int:

