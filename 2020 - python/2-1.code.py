import re

pattern = r"(\d+)\-(\d+) (.+)\: (.+)"
with open("2-1.input.txt") as input:
    lines = input.readlines()
    i = 0

    for line in lines:
        match = re.match(pattern, line)

        if (match):

            min_range = int(match.group(1))
            max_range = int(match.group(2))
            character = match.group(3)
            password = match.group(4)

            counter = password.count(character)

            if (counter <= max_range and counter >= min_range):
                i += 1

    print(i)
