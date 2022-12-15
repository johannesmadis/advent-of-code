import re

lines = [line for line in open("14.input.txt").read().split("\n")]


def numberToBase(n, b):
    if n == 0:
        return [0]
    digits = []
    while n:
        digits.append(int(n % b))
        n //= b
    return digits[::-1]


memory = {}
mask = ""

value = 74


pattern = re.compile(r"mem\[(\d+)\]")


def write_to_address(address: int, value: int, mask: list):
    value_base_2 = [str(item) for item in numberToBase(int(value), 2)]

    padding = [0] * (36 - len(value_base_2))

    padded_value = padding + value_base_2

    for index, value in enumerate(mask):
        if (value != "X"):
            padded_value[index] = value
    memory[address] = int("".join([str(item) for item in padded_value]), 2)


def write_to_address2(address: int, value: int, mask: list):
    address_base_2 = [str(item) for item in numberToBase(int(address), 2)]
    padding = [0] * (36 - len(address_base_2))

    padded_address = padding + address_base_2

    addresses = []

    def apply(base, apply_mask, start):
        for index in range(start, len(mask)):
            mask_item = mask[index]
            if (mask_item == "1"):
                base[index] = "1"
            elif(mask_item == "X"):
                # apply 0 to current
                # apply 1 to copy
                new_base = [item for item in base]
                base[index] = "0"
                new_base[index] = "1"
                apply(new_base, mask, index + 1)

        addresses.append(base)

    apply(padded_address, mask, 0)

    for address in addresses:
        int_address = int("".join([str(item) for item in address]), 2)
        memory[int_address] = int(value)


for line in lines:
    assignment = line.split(" = ")

    command = assignment[0]
    value = assignment[1]

    if command == "mask":
        mask = list(value)
    else:
        address = re.match(pattern, command)
        if address is not None:
            mem_address = int(address[1])
            write_to_address2(mem_address, value, mask)

print(sum(memory.values()))
