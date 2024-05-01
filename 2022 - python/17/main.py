ROUNDS = 2022


SHAPES = [
    ((1, 1, 1, 1),),
    ((0, 1, 1), (1, 1, 1), (0, 1, 0)),
    ((0, 0, 1), (0, 0, 1), (1, 1, 1)),
    ((1,), (1,), (1,), (1,)),
    ((1, 1), (1, 1)),
]

LEFT = "<"
RIGHT = ">"

EMPTY_LINE = [1, 0, 0, 0, 0, 0, 0, 1]


class Chamber:
    def __init__(self):
        self.current_round = 0
        self.shape_index = 0
        self.current_item = None
        self.current_item_pos = (0, 0)
        self.falling_mode = False  # 0 is horizontal, 1 is vertical
        self.pattern = ""
        self.map = [EMPTY_LINE.copy()]

        with open("input.test.txt") as input_file:
            self.pattern = input_file.read()

        self.pattern_length = len(self.pattern)

    def get_next_shape(self):
        self.current_item = SHAPES[self.shape_index % len(SHAPES)]
        self.shape_index += 1
        self.falling_mode = False  # rset falling mode
        top_row = self.get_top_row()
        rows_to_add = top_row + 3 + len(self.current_item) - len(self.map)
        if rows_to_add > 0:
            for i in range(rows_to_add):
                self.map.append(EMPTY_LINE.copy())
        self.current_item_pos = (top_row + 3, 3)  # because 9-wide not 7

    def intersects(self):
        intersects = False
        for ri, row in enumerate(self.current_item):
            for ci, c in enumerate(row):
                x = ci + self.current_item_pos[0]
                y = ri + self.current_item_pos[1]
                if len(self.map) > y:
                    continue
                if c == 1 and self.map[y][x] == 1:
                    intersects == True
                    break
            if intersects == True:
                break

        return intersects

    def run(self):
        for round_index in range(ROUNDS):
            self.current_round += 1
            self.step()

    def step(self):
        # if no current item, take next

        if self.current_item is None:
            self.get_next_shape()

        if self.falling_mode is True:
            self.down()
            if self.intersects():
                self.freeze()
        else:
            index = self.current_round // 2
            direction = self.pattern[index % self.pattern_length]

            if direction == LEFT:
                self.left()
                if self.intersects():
                    self.right()
            elif direction == RIGHT:
                self.right()
                if self.intersects():
                    self.left()

        self.falling_mode = not self.falling_mode

    def left(self):
        self.current_item_pos = (self.current_item_pos[0] + 1, self.current_item_pos[1])

    def right(self):
        self.current_item_pos = (self.current_item_pos[0] - 1, self.current_item_pos[1])

    def down(self):
        self.current_item_pos = (self.current_item_pos[0], self.current_item_pos[1] - 1)

    def freeze(self):
        for ri, row in enumerate(self.current_item):
            for ci, c in enumerate(row):
                x = ci + self.current_item_pos(0)
                y = ri + self.current_item_pos(0)
                if c == 1:
                    self.map[y][x] = 1
        self.current_item = None

    def get_top_row(self):
        top_row = 0
        for index, line in enumerate(self.map):
            if sum(line) == 2:  # first and last always there, giving sum of 2
                top_row = index - 1
        return top_row


chamber = Chamber()
chamber.run()

print(chamber.get_top_row())
