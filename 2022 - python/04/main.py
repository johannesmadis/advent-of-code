def main(lines):
    contains = 0
    overlaps = 0

    for line in lines:
        [a, b] = line.split(",")
        [a1, a2] = [int(x) for x in a.split("-")]
        [b1, b2] = [int(x) for x in b.split("-")]

        if (a1 <= b1 and a2 >= b2) or (b1 <= a1 and b2 >= a2):
            contains += 1

        if (a1 <= b1 and a2 >= b1) or (b1 <= a1 and b2 >= a1):
            overlaps += 1

    print(contains)
    print(overlaps)


with open("C:/Users/johan/Documents/aoc-20222/04/input.txt") as input:
    input_lines = input.readlines()
    main(input_lines)
