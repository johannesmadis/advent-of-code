from __future__ import annotations
from typing import List
import copy
import math


class Cell:
    SEAT = "L"
    FLOOR = "."
    PERSON = "#"

    def __init__(self, cell_type: str, row: int, col: int) -> None:
        self.set_type(cell_type)
        self.row = row
        self.col = col

    def set_type(self, cell_type: str) -> Cell:
        self.type = cell_type
        self.is_seat = cell_type == Cell.SEAT
        self.is_floor = cell_type == Cell.FLOOR
        self.is_person = cell_type == Cell.PERSON

        return self


class Clonable:
    def clone(self) -> Clonable:
        return copy.deepcopy(self)


class Grid(Clonable):
    DIRECTIONS = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                  (0, 1), (1, -1), (1, 0), (1, 1))

    def __init__(self, dim_row: int, dim_col: int) -> None:
        self.items = []
        self.dim_row = dim_row
        self.dim_col = dim_col
        for item_index in range(dim_row * dim_col):
            col = item_index % dim_col
            row = math.floor(item_index / dim_col)
            self.items.append(Cell(Cell.FLOOR, row, col))

    def get(self, row: int, col: int) -> Cell or None:
        index = row * self.dim_col + col
        if (index < len(self.items) and index >= 0):
            return self.items[index]
        return None

    def set(self, row: int, col: int, cell_type: str) -> Cell or None:
        item = self.get(row, col)
        if (item is not None):
            item.set_type(cell_type)
        return item

    def print(self) -> Grid:
        for row_index in range(self.dim_row):
            start = row_index * self.dim_col
            end = start + self.dim_col
            print(''.join([cell.type for cell in self.items[start:end]]))
        return self

    def count_neighbor(self, cell: Cell) -> int:
        return self.count_visible_neighbor(cell, 1)

    def count_visible_neighbor(self, cell: Cell, limit: int = math.inf) -> int:
        counter = 0

        for direction in Grid.DIRECTIONS:
            index = 0
            while index < limit:
                index += 1
                current_row = cell.row + direction[0] * index
                current_col = cell.row + direction[1] * index
                item = self.get(current_row, current_col)
                if (item is None):
                    break
                elif(item.is_seat):
                    break
                elif (item.is_person):
                    counter += 1
                    break

        return counter


class Input:
    def __init__(self, file_name: str) -> None:
        self.file_name = file_name
        self.content = None
        self.lines = None

    def read(self) -> str:
        with open(self.file_name) as f:
            self.content = f.read()
        return self.content

    def read_lines(self) -> List[str]:
        if (self.content is None):
            self.read()

        if (self.lines is None):
            self.lines = self.content.split("\n")
        return self.lines


seats = Input("11.input.txt")
seats.read_lines()

grid = Grid(len(seats.lines), len(seats.lines[0]))

for line_index, line in enumerate(seats.lines):
    for char_index, char in enumerate(line):
        grid.set(line_index, char_index, char)


grid.clone().print()
