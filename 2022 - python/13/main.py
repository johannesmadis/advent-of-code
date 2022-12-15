import functools
input = """[1,1,3,1,1]
[1,1,5,1,1]

[[1],[2,3,4]]
[[1],4]

[9]
[[8,7,6]]

[[4,4],4,4]
[[4,4],4,4,4]

[7,7,7,7]
[7,7,7]

[]
[3]

[[[]]]
[[]]

[1,[2,[3,[4,[5,6,7]]]],8,9]
[1,[2,[3,[4,[5,6,0]]]],8,9]"""


with open("input.txt") as input_file:
    input = input_file.read()


def compare(left, right):
    if isinstance(left, int) and isinstance(right, int):
        if left == right:
            return 0
        if left < right:
            return 1
        if left > right:
            return -1
    if isinstance(left, list) and isinstance(right, list):

        for i, (l, r) in enumerate(zip(left, right)):
            result = compare(l, r)
            #print(f"{i}: {l} ? {r} = {result}")
            if result == 1:
                return result
            if result == -1:
                return result

            # else 0, continue but also check if i is len(l) -1 but not len(r)-1
            if i == len(left)-1 and i != len(right)-1:
                return 1
            if i != len(left)-1 and i == len(right)-1:
                return -1

        # case if any of them were empty lists and loop didnt happen
        if len(left) < len(right):
            return 1
        if len(right) < len(left):
            return -1
        return 0

    if isinstance(left, list) and not isinstance(right, list):
        return compare(left, [right])
    if not isinstance(left, list) and isinstance(right, list):
        return compare([left], right)


pair_strings = input.split("\n\n")
pairs = [pair_str.split("\n") for pair_str in pair_strings]

i = 0
indices = []
for pair in pairs:
    i += 1

    left = eval(pair[0])
    right = eval(pair[1])

    # print("")
    correct_order = compare(left, right)
    #print(f"Order: {correct_order}")

    if correct_order == 1:
        indices.append(i)

print("")
print(indices, sum(indices))

# part 2

decoder_packets = [[[2]], [[6]]]
packets_list = [eval(line.strip())
                for line in input.split("\n") if line.strip() != ""]
packets_list.extend(decoder_packets)


sorted_packets = sorted(
    packets_list, key=functools.cmp_to_key(compare), reverse=True)
indices = [sorted_packets.index(decoder) + 1 for decoder in decoder_packets]


print(indices[0]*indices[1])
