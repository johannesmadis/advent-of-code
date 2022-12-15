
class Task:
    def __init__(self, delta, delay):
        self.delta = delta
        self.delay = delay
        self.done = False

    def __str__(self):
        return f"Task ({self.delta}, {self.delay})"


class Clock:
    off = "  "
    on = "[]"
    rows = 6
    cols = 40

    def __init__(self):
        self.lines = []
        self.signals = []
        self.tick = 0
        self.X = 1

        self.display = [Clock.off]*Clock.cols*Clock.rows

    def run(self):
        for task in self.lines:
            for _ in range(task.delay):

                # for part2
                # if self.X nearby current tick, change display
                delta = self.X - (self.tick % Clock.cols)
                if delta >= -1 and delta <= 1:
                    self.display[self.tick] = Clock.on

                self.tick += 1

                # for part1

                if (self.tick - 20) % 40 == 0:
                    self.signals.append((self.tick, self.X))

            self.X += task.delta

    def print_display(self):
        for i in range(Clock.rows):
            line = "".join(self.display[i*Clock.cols:(i+1)*Clock.cols])
            print(line)


clock = Clock()

with open("input.txt") as file_input:
    lines = file_input.readlines()
    for line in lines:
        cmd = line.split(" ")
        if cmd[0].strip() == "addx":
            clock.lines.append(Task(int(cmd[1].strip()), 2))
        elif cmd[0].strip() == "noop":
            clock.lines.append(Task(0, 1))


clock.run()
print(sum([x[0]*x[1] for x in clock.signals]))
clock.print_display()
