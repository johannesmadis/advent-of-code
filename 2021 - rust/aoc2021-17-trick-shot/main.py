from __future__ import annotations
"""
test_input = "target area: x=20..30, y=-10..-5"
input = "target area: x=153..199, y=-114..-75"
"""


class domain:
    def __init__(self, start, stop, step=1):
        self.start = start
        self.stop = stop
        self.step = step
        self.range = range(start, stop, step)

    def contains(self, x: float):
        return self.start <= x and self.stop > x


target_x = domain(153, 199 + 1)
target_y = domain(-114, -75 + 1)


def part1(yf_min):
    vy = (abs(yf_min) - 1)
    h_max = ((vy + 0.5) ** 2) / 2
    return round(h_max)


max_y = part1(-114)

stack = []
position = [0, 0]

for initial_x_vel in range(1, target_x.stop + 1):
    for initial_y_vel in range(target_y.start, max_y):
        x_vel = initial_x_vel
        y_vel = initial_y_vel
        position[0] = 0
        position[1] = 0

        while target_x.stop >= (position[0] + x_vel) and target_y.start >= (position[1] + y_vel):
            position[0] += x_vel
            position[1] += y_vel

            if target_x.contains(position[0]) and target_y.contains(position[1]):
                stack.append((x_vel, y_vel, position[0], position[1]))
                break

            if x_vel > 0:
                x_vel -= 1

            y_vel -= 1


"""
    while (position[0] + x_vel) < target_x.stop and (position[1] + y_vel) > target_y.start:
        position[0] += x_vel
        position[1] += y_vel

        if x_vel > 0:
            x_vel -= 1
        y_vel -= 1
    """

y_stack = [item[1] for item in stack]
print(max(y_stack))
print(len(y_stack))

print(len(stack))

print(part1(-114))
