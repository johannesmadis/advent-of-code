import re

lines = []

with open("./input.txt") as input_file:
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]


class Block:
    def __init__(self, row, start, data):
        self.data = data
        self.row = row
        self.start = start
        self.len = 1

    def append(self, data):
        self.data += data
        self.len += 1

    def get_neighbors(self, rowlist):
        neighbors = []

        n_start_col = self.start - 1
        if n_start_col < 0:
            n_start_col = 0

        n_end_col = self.start + self.len + 1
        if n_end_col >= len(rowlist[0]):
            n_end_col = len(rowlist[0]) - 1

        prev_row = self.row - 1
        next_row = self.row + 1

        if prev_row >= 0:
            neighbors.append(rowlist[prev_row][n_start_col:n_end_col])

        if next_row < len(rowlist):
            neighbors.append(rowlist[next_row][n_start_col:n_end_col])

        if self.start > 0:
            neighbors.append(rowlist[self.row][self.start - 1])

        if self.start + self.len < len(rowlist[0]) - 1:
            neighbors.append(rowlist[self.row][self.start + self.len])

        return neighbors

    def get_neighbors_with_positions(self, rowlist):
        neighbors = []

        n_start_col = self.start - 1
        if n_start_col < 0:
            n_start_col = 0

        n_end_col = self.start + self.len + 1
        if n_end_col >= len(rowlist[0]):
            n_end_col = len(rowlist[0]) - 1

        prev_row = self.row - 1
        next_row = self.row + 1

        if prev_row >= 0:
            for charIndex, char in enumerate(rowlist[prev_row][n_start_col:n_end_col]):
                if char == "*":
                    neighbors.append((complex(n_start_col + charIndex, prev_row), char))

        if next_row < len(rowlist):
            for charIndex, char in enumerate(rowlist[next_row][n_start_col:n_end_col]):
                if char == "*":
                    neighbors.append((complex(n_start_col + charIndex, next_row), char))

        if self.start > 0 and rowlist[self.row][self.start - 1] == "*":
            neighbors.append(
                (complex(self.start - 1, self.row), rowlist[self.row][self.start - 1])
            )

        if (
            self.start + self.len < len(rowlist[0]) - 1
            and rowlist[self.row][self.start + self.len] == "*"
        ):
            neighbors.append(
                (
                    complex(self.start + self.len, self.row),
                    rowlist[self.row][self.start + self.len],
                )
            )

        return neighbors

    def has_symbol_neighbor(self, rowlist):
        neighbors = self.get_neighbors(rowlist)

        print(self.data, neighbors)

        has_symbol_neighbor = False
        for neighbor_group in neighbors:
            if has_symbol_neighbor:
                break
            for char in neighbor_group:
                if char != "." and not char.isnumeric():
                    has_symbol_neighbor = True
                    break

        return has_symbol_neighbor

    def get_gears(self, rowlist):
        neighbors = self.get_neighbors_with_positions(rowlist)

        return neighbors


blocks = []
for index, line in enumerate(lines):
    currentBlock = None
    for col, char in enumerate(line):
        if char.isnumeric():
            if currentBlock is None:
                currentBlock = Block(index, col, char)
                blocks.append(currentBlock)
            else:
                currentBlock.append(char)
        else:
            currentBlock = None


symbol_blocks = [
    int(block.data) for block in blocks if block.has_symbol_neighbor(lines)
]
print(sum(symbol_blocks))


gear_list = {}
gear_sum = 0

for block in [block for block in blocks if block.has_symbol_neighbor(lines)]:
    gears = block.get_gears(lines)
    for gear in gears:
        gear_list.setdefault(gear[0], [])
        gear_list[gear[0]].append(block)

for gear_pos in gear_list:
    gear = gear_list[gear_pos]
    if len(gear) == 2:
        gear_sum += int(gear[0].data) * int(gear[1].data)

print("gear sum", gear_sum)
