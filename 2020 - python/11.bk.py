

with open("11.input.txt") as f:
    content = f.read().split("\n")
    for lineIndex, line in enumerate(content):
        base_grid.append([])
        for charIndex, char in enumerate(line):
            base_grid[lineIndex].append(char)


def count_neighbors(row, col, grid):
    grid_length = len(grid)
    grid_width = len(grid[0])

    counter = 0

    for neighbor_row in range(row - 1, row + 2, 1):
        # add ifs
        if (neighbor_row < grid_length and neighbor_row >= 0):
            for neighbor_col in range(col - 1, col + 2, 1):
                # add ifs
                if (neighbor_col < grid_width and neighbor_col >= 0 and not (neighbor_col == col and neighbor_row == row)):
                    neighbor_cell = grid[neighbor_row][neighbor_col]
                    if (neighbor_cell == PERSON):
                        counter += 1

    return counter


directions = ((-1, -1), (-1, 0), (-1, 1), (0, -1),
              (0, 1), (1, -1), (1, 0), (1, 1))


def count_visible_neighbors(row, col, grid):

    counter = 0

    grid_length = len(grid)
    grid_width = len(grid[0])

    for direction in directions:
        sight_round = 0
        while (True):
            sight_round += 1
            check_row = row + direction[0] * sight_round
            check_col = col + direction[1] * sight_round
            if (check_row < grid_length and check_col < grid_width and check_row >= 0 and check_col >= 0):
                check_cell = grid[check_row][check_col]
                if (check_cell == FLOOR):
                    continue
                elif (check_cell == PERSON):
                    counter += 1
                    break
                elif (check_cell == SEAT):
                    break
            else:
                break
    return counter


def seating_round(old_grid):
    new_grid = copy.deepcopy(old_grid)
    changes = 0

    for lineIndex, line in enumerate(new_grid):
        for cellIndex, cell in enumerate(line):
            count_neighbor = count_neighbors(
                lineIndex, cellIndex, old_grid)

            if (cell == FLOOR):
                continue
            elif (cell == SEAT):
                if (count_neighbor == 0):
                    new_grid[lineIndex][cellIndex] = PERSON
                    changes += 1
            elif (cell == PERSON):
                if (count_neighbor >= 4):
                    new_grid[lineIndex][cellIndex] = SEAT
                    changes += 1

    return new_grid, changes


def seating_round2(old_grid):
    new_grid = copy.deepcopy(old_grid)
    changes = 0

    for lineIndex, line in enumerate(new_grid):
        for cellIndex, cell in enumerate(line):
            count_neighbor = count_visible_neighbors(
                lineIndex, cellIndex, old_grid)

            if (cell == FLOOR):
                continue
            elif (cell == SEAT):
                if (count_neighbor == 0):
                    new_grid[lineIndex][cellIndex] = PERSON
                    changes += 1
            elif (cell == PERSON):
                if (count_neighbor >= 5):
                    new_grid[lineIndex][cellIndex] = SEAT
                    changes += 1

    return new_grid, changes


def count_seats(grid):
    counter = 0
    for line in grid:
        for cell in line:
            if cell == PERSON:
                counter += 1

    return counter


def print_grid(grid):
    for line in grid:
        print(line)


change_count = -1
start_grid = base_grid
round_counter = 0
while (change_count != 0):

    start_grid, change_count = seating_round2(start_grid)
    # print(change_count, count_seats(start_grid)
    #      )
    round_counter += 1


print(round_counter, count_seats(start_grid))
