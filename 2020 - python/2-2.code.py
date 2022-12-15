import re

pattern = r"(\d+)\-(\d+) (.+)\: (.+)"
with open("2-1.input.txt") as input:
    lines = input.readlines()
    i = 0

    for line in lines:
        match = re.match(pattern, line)

        if (match):

            first_position = int(match.group(1)) - 1
            second_position = int(match.group(2)) - 1
            character = match.group(3)
            password = match.group(4)

            char_0 = password[first_position]
            char_1 = password[second_position]

            if ((character == char_0 or char_1 == character) and char_0 != char_1):
                i += 1

    print(i)
