from __future__ import annotations
from typing import List
import time

UP = "\033[A"


class Printer:
    def __init__(self, w: int, h: int):
        data = [[" "] * w]*h

        for row in data:
            line = "".join(row)
            print(line)

    def print(self, data: List[str]) -> None:
        # go up self.h lines
        for _ in range(len(data)):
            print("", end=UP)

        for row in data:
            print(row)


printer = Printer(4, 4)

printer.print(["qwer", "wert", "erty", "rtyu"])
time.sleep(5)
printer.print(["wert", "erty", "rtyu", "qwer"])
