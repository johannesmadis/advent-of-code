import re

lines = []

with open("./input.txt") as input_file:
    lines = input_file.readlines()
    lines = [line.strip() for line in lines]


cards = []

for line in lines:
    index, data = line.split(": ")

    winning_str, guess_str = data.split(" | ")
    winning_set = set([int(num) for num in re.findall(r"(\d+)", winning_str)])
    guess_set = set([int(num) for num in re.findall(r"(\d+)", guess_str)])
    cards.append((winning_set, guess_set))


total = 0
for winning, guess in cards:
    intersection = winning.intersection(guess)
    points = 0
    if len(intersection) > 0:
        points += pow(2, len(intersection) - 1)
    total += points

print(total)


card_counts = {}

for index, (winning, guess) in enumerate(cards):
    card_counts.setdefault(index, 1)
    current_count = card_counts[index]

    intersection = winning.intersection(guess)
    matching_number_count = len(intersection)
    for i in range(matching_number_count):
        card_counts.setdefault(index + i + 1, 1)
        card_counts[index + i + 1] += 1 * current_count

print(sum([card_counts[key] for key in card_counts]))
