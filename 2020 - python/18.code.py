import re


# class to mask - to *


class a(int):
    # mask * to +
    def __mul__(self, b):
        return a(int(self) + b)

    def __add__(self, b):
        return a(int(self) + b)

    # mask * -
    def __sub__(self, b):
        return a(int(self) * b)


def calculate(input_str, part_2=False):
    expr = input_str.replace("*", "-")
    if part_2 is True:
        expr = expr.replace("+", "*")
    expr = re.sub(r"(\d+)", r"a(\1)", expr)
    return eval(expr, {}, {"a": a})


input_expressions = open("18.input.txt").read().split("\n")

print(sum([calculate(item, True) for item in input_expressions]))
