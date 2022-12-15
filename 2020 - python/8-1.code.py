class Game:
    def __init__(self):
        self.value = 0
        self.current_index = 0
        self.visited_indices = {}
        self.inputs = []
        self.loop_termination = False

    def acc(self, value):
        self.value += value
        self.current_index += 1

    def jmp(self, value):
        self.current_index += value

    def nop(self, value):
        self.current_index += 1

    def do(self, command, value):
        if (command == "acc"):
            self.acc(value)
        elif(command == "jmp"):
            self.jmp(value)
        elif (command == "nop"):
            self.nop(value)

    def setup(self, lines):
        for line in lines:
            cmd = line.split(" ")
            self.inputs.append({"command": cmd[0], "value": int(cmd[1])})

    def run(self):
        while ((self.current_index not in self.visited_indices) and (len(self.inputs) > self.current_index)):
            local_current_index = self.current_index
            self.do(self.inputs[self.current_index]["command"],
                    self.inputs[self.current_index]["value"])
            self.visited_indices[local_current_index] = True
        if(len(self.inputs) > self.current_index):
            self.loop_termination = True


with open("8-1.input.txt") as f:
    content = f.read()
    lines = content.split("\n")

    count = len(lines)
    for index in range(count):
        game = Game()

        current_line = lines[index]
        command = current_line.split(" ")
        new_command = current_line

        if (command[0] == "jmp"):
            new_command = "nop " + str(command[1])
        elif (command[0] == "nop"):
            new_command == "jmp " + str(command[1])

        lines[index] = new_command

        game.setup(lines)
        lines[index] = current_line

        game.run()
        if (not game.loop_termination):
            print(str(index) + ": " + str(game.value))
