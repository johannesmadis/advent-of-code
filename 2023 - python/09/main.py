lines = []
with open("./input.txt") as input_file:
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]

col_count = len(lines[0])
line_count = len(lines)


def get_neighbor_indices(current):
    neighbors = []

    if current[0] != 0:
        lines.append((current[0] - 1, current[1]))
    if current[0] != line_count - 1:
        lines.append((current[0] + 1, current[1]))

    if current[1] != 0:
        lines.append((current[0], current[1] - 1))
    if current[1] != col_count:
        lines.append((current[0], current[1] + 1))

    return neighbors


def find_start():
    start_pos = (0, 0)

    for line_index, line in enumerate(lines):
        for col_index, col in enumerate(line):
            if col == "S":
                start_pos = (line_index, col_index)  # y,x
                break
    return start_pos


def get_symbol(point):
    return lines[point[0]][point[1]]


def part1():
    start = find_start()
    
    neighbors = get_neighbor_indices(start)
    for neighbors in neighbors:
        


part1()
