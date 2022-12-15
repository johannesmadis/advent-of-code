
"""
            [Q]     [G]     [M]    
            [B] [S] [V]     [P] [R]
    [T]     [C] [F] [L]     [V] [N]
[Q] [P]     [H] [N] [S]     [W] [C]
[F] [G] [B] [J] [B] [N]     [Z] [L]
[L] [Q] [Q] [Z] [M] [Q] [F] [G] [D]
[S] [Z] [M] [G] [H] [C] [C] [H] [Z]
[R] [N] [S] [T] [P] [P] [W] [Q] [G]
 1   2   3   4   5   6   7   8   9 
"""
import re


def parse_stacks(initial_stacks):
    initial_line_length = len(initial_stacks[-1])
    n_stacks = int((initial_line_length + 1) / 4)

    indices_of_stacks = [i*4+1 for i in range(n_stacks)]

    stacks = []
    for s in range(n_stacks):
        stacks.append([])

    for stack_line in initial_stacks:
        for i, stack_char_index in enumerate(indices_of_stacks):
            character = stack_line[stack_char_index]
            if character != " ":
                stacks[i].append(stack_line[stack_char_index])

    return stacks


def step(stacks, instruction_line):
    amount, index_from, index_to = [
        int(x) for x in re.findall("(\d+)", instruction_line)]

    print("amount", amount, index_from, index_to)

    items = stacks[index_from-1][-amount:]
    del stacks[index_from-1][-amount:]
    stacks[index_to-1].extend(items)

    print("Step")
    for stack in stacks:
        print(stack)

    """


    amount, index_from, index_to = re.findall("(\d+)", instruction_line)

    for _ in range(int(amount)):
        item = stacks[int(index_from)-1].pop()
        stacks[int(index_to)-1].append(item)
    """


with open("C:\\Users\\johan\\Documents\\aoc-20222\\04\\05\\input.txt") as input:
    [initial, steps] = input.read().split("\n\n")

    initial_stacks = initial.split("\n")
    initial_stacks.pop()  # remove indices line
    initial_stacks.reverse()
    stacks = parse_stacks(initial_stacks)

    step_lines = steps.split("\n")
    for step_instruction in step_lines:
        step(stacks, step_instruction)

    for stack in stacks:
        print(stack)
    result = [x[-1] if len(x) > 0 else "" for x in stacks]

    print(result)
