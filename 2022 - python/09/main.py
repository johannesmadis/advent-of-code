inputs = ""
with open("input.txt") as input_file:
    inputs = input_file.read()


class Snake:
    def __init__(self):
        # x + yj
        self.head_position = 0 + 0j
        self.tail_position = 0 + 0j
        self.tail_history = {self.tail_position}  # set

    def up(self):
        self.head_position += 1j
        self.update_tail()

    def down(self):
        self.head_position -= 1j
        self.update_tail()

    def left(self):
        self.head_position -= 1
        self.update_tail()

    def right(self):
        self.head_position += 1
        self.update_tail()

    def update_tail(self):

        delta = self.head_position - self.tail_position

        x_delta = delta.real
        y_delta = delta.imag

        if abs(x_delta) == 2 and y_delta == 0:  # horizontal
            self.tail_position += 1 if x_delta > 0 else -1
        elif abs(y_delta) == 2 and x_delta == 0:  # vertical
            self.tail_position += 1j if y_delta > 0 else -1j
        elif (abs(x_delta) == 2 and abs(y_delta) in (1, 2)) or (abs(y_delta) == 2 and abs(x_delta) in (1, 2)):
            self.tail_position += complex(1 if x_delta >
                                          0 else -1, 1 if y_delta > 0 else -1)

        self.tail_history.add(self.tail_position)

    def print(self):
        board_range_max = complex(max(self.head_position.real, self.tail_position.real, 0, *[history.real for history in self.tail_history]), max(
            self.head_position.imag, self.tail_position.imag, *[history.imag for history in self.tail_history]))
        board_range_min = complex(min(self.head_position.real, self.tail_position.real, 0, *[history.real for history in self.tail_history]), min(
            self.head_position.imag, self.tail_position.imag, 0, *[history.imag for history in self.tail_history]))

        delta = board_range_max - board_range_min

        for y in range(int(delta.imag)):
            print("".join(["#" if complex(
                x, delta.imag - y) in self.tail_history else "." for x in range(int(delta.real))]))


# part1
snake = Snake()

for line in [line.strip() for line in inputs.split("\n")]:
    [direction, count_str] = line.split(" ")

    for _ in range(int(count_str)):
        if direction == "U":
            snake.up()
        elif direction == "D":
            snake.down()
        elif direction == "L":
            snake.left()
        elif direction == "R":
            snake.right()
print(len(snake.tail_history))

# part10


snakes = [Snake() for _ in range(9)]
snake_head = snakes[0]
snake_tail = snakes[-1]

for line in [line.strip() for line in inputs.split("\n")]:
    [direction, count_str] = line.split(" ")

    for _ in range(int(count_str)):
        if direction == "U":
            snake_head.up()
        elif direction == "D":
            snake_head.down()
        elif direction == "L":
            snake_head.left()
        elif direction == "R":
            snake_head.right()

        for i, snake_link in enumerate(snakes[1:]):
            # 0 to 8 which corresponds to source snake index
            previous_link = snakes[i]
            snake_link.head_position = previous_link.tail_position
            snake_link.update_tail()

print(len(snake_tail.tail_history))
