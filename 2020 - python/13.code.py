import re
import math

lines = [line for line in open("13.input.txt").read().split("\n")]

min_boundary = int(lines[0])
buses = [bus for bus in lines[1].split(",")]

min_waiting = math.inf
result = -1
for bus in buses:
    if bus != "x":
        bus_id = int(bus)
        earliest = math.ceil(min_boundary / bus_id) * bus_id
        if (earliest < min_waiting):
            min_waiting = earliest
            result = (earliest - min_boundary) * bus_id


t = 0
s = 1
i = 0
while i < len(buses):
    bus = buses[i]
    if (bus == "x"):
        i += 1
        continue

    if ((t+i) % int(bus) == 0):
        s *= int(bus)
        i += 1
        continue

    t += s


print(t)

"""
0 29        t % 29 = 0
23 37       t % 37 = 23
29 433      t % 433 = 29
42 13       t % 13 = 42
43 17       t % 17 = 43
48 19       t % 19 = 48
52 23       t % 23 = 52
60 977      t % 977 = 60
101 41      t % 41 = 101
"""

# 100000000000111
#  43838520894961
