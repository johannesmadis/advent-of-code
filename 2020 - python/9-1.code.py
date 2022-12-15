preamble = 25

with open("9-1.input.txt") as f:
    content = f.read()
    lines = content.split("\n")

    invalid = -1

    for index in range(preamble, len(lines)):
        has_result = False
        for a in range(index - preamble, index):
            for b in range(a, a + preamble):
                item_a = int(lines[a])
                item_b = int(lines[b])
                result = item_a + item_b
                if (result == int(lines[index])):
                    has_result = True
        if (has_result):
            continue
        else:
            invalid = int(lines[index])
            break

    # for each item, while sum smaller than invalid, add next
    # if same as invalid, success
    # if larger, continue
    needed_result = invalid  # 257342611

    print("invalid " + str(invalid))

    has_result = False
    added_numbers = []

    for index in range(len(lines)):
        if (has_result == True):
            break

        value = 0
        base = int(lines[index])
        added_numbers = []

        for a_index in range(index, len(lines)):
            a = int(lines[a_index])
            value += a
            added_numbers.append(a)
            if (value == needed_result):
                has_result = True
                break
            elif (value > needed_result):
                break
            elif (value < needed_result):
                continue

    smallest = min(added_numbers)
    largest = max(added_numbers)
    print(smallest + largest)
