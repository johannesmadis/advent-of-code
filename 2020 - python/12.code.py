from __future__ import annotations
import re
import math
from Input import Input


class Ship:
    PATTERN = re.compile(r"(.)(\d+)")

    def __init__(self) -> None:
        self.x = 0
        self.y = 0
        self.wx = 10
        self.wy = 1

    def move(self, cmd: str) -> Ship:
        commands = re.match(Ship.PATTERN, cmd)
        if (commands is not None):
            command = commands[1]
            value = int(commands[2])
            if (command in ("L", "R")):
                self.turn(command, value)
            elif (command == "F"):
                self.forward(value)
            elif (command == "N"):
                self.wy += value
            elif (command == "S"):
                self.wy -= value
            elif (command == "E"):
                self.wx += value
            elif (command == "W"):
                self.wx -= value
        print(cmd, self.x, self.y, self.wx, self.wy)
        return self

    def turn(self, dir: str, degrees: int) -> Ship:
        normalised_degrees = degrees if dir == "L" else 360 - degrees
        sin_map = {90: 1, 180: 0, 270: -1}
        cos_map = {90: 0, 180: -1, 270: 0}

        x = cos_map[normalised_degrees] * self.wx - \
            sin_map[normalised_degrees] * self.wy
        y = sin_map[normalised_degrees] * self.wx + \
            cos_map[normalised_degrees] * self.wy

        self.wx = x
        self.wy = y

        return self

    def forward(self, value: int) -> Ship:
        self.x += self.wx * value
        self.y += self.wy * value
        return self

    def manhattan(self) -> int:
        return abs(self.x) + abs(self.y)


ship = Ship()
commands = Input("12.input.txt").read_lines()
for command in commands:
    ship.move(command)

print(ship.x, ship.y, ship.manhattan())
