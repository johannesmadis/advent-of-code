import math

# 2,1,6,3,4


class Item:
    primes = (2, 3, 5, 7, 11, 13, 17, 19, 23)
    lcm = math.prod(primes)

    def __init__(self, value):
        self.value = value
        self.divisors = []
        self.reduce()

    def inspect(self, divisible):
        return self.value % divisible == 0

    def operation(self, fn):
        return Item(fn(self.value))

    def reduce(self):
        self.value %= Item.lcm

    def compress(self):
        #  print(self.value, self.divisors, self.value * math.prod(self.divisors))
        return self.value


class Monkey:
    registry = []

    def __init__(self, starting_items, op, divisible, target_true, target_false):
        self.items = [Item(x) for x in starting_items]
        self.op = op
        self.divisible = divisible
        self.target_true = target_true
        self.target_false = target_false
        self.inspect_count = 0
        Monkey.registry.append(self)

    def inspect(self):
        # operation (worry level increase)
        self.inspect_count += len(self.items)

        # inspection (op) and worry level decrease /3
        items = [item.operation(self.op) for item in self.items]

        # test (get target)
        targets = [self.target_true if item.inspect(
            self.divisible) else self.target_false for item in items]

        for item, target in zip(items, targets):
            self.give(item, target)

        # all have been given away, items is empty
        self.items = []

    def give(self, item, target):
        Monkey.registry[target].receive(item)

    def receive(self, item):
        self.items.append(item)


# test
"""
Monkey([79, 98], lambda x: x * 19, 23, 2, 3),
Monkey([54, 65, 75, 74], lambda x: x+6, 19, 2, 0),
Monkey([79, 60, 97], lambda x: x*x, 13, 1, 3),
Monkey([74], lambda x: x+3, 17, 0, 1)

"""
# real


Monkey([97, 81, 57, 57, 91, 61], lambda x: x * 7, 11, 5, 6),
Monkey([88, 62, 68, 90], lambda x: x*17, 19, 4, 2),

Monkey([74, 87], lambda x: x+2, 5, 7, 4),

Monkey([53, 81, 60, 87, 90, 99, 75], lambda x: x+1, 2, 2, 1)

Monkey([57], lambda x: x+6, 13, 7, 0),

Monkey([54, 84, 91, 55, 59, 72, 75, 70], lambda x: x*x, 7, 6, 3),

Monkey([95, 79, 79, 68, 78], lambda x: x+3, 3, 1, 3)

Monkey([61, 97, 67], lambda x: x+4, 17, 0, 5)


for round in range(10000):
    for monkey in Monkey.registry:
        monkey.inspect()


monkey_business = [x.inspect_count for x in Monkey.registry]
# monkey_business.sort(reverse=True)


print("")
print(monkey_business)
monkey_business.sort(reverse=True)
print(monkey_business[0]*monkey_business[1])
