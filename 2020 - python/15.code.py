import re

lines = [line for line in open("15.input.txt").read().split("\n")]

puzzle_input = [2, 0, 6, 12, 1, 3]
test_input = [2, 0, 6, 12, 1, 3]
memory = {}

last_input = -1


rounds = 2020
for counter, starting in enumerate(test_input):
    memory[starting] = [counter, counter]

for round_index in range(6, 30000000):
    num = test_input[round_index-1]  # base num
    if num in memory:
        memory[num][1] = memory[num][0]
        memory[num][0] = round_index-1
    else:
        memory[num] = [round_index-1, round_index-1]
    next_num = memory[num][0] - memory[num][1]
    test_input.append(next_num)


print(test_input[-1])
