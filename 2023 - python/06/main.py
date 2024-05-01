def is_count(item, count, exclude="X"):
    for key in item:
        if item[key] == count and key != exclude:
            return True
    return False


def is_two_pairs(item):
    pair_count = 0
    for key in item:
        if item[key] == 2:
            pair_count += 1
    return pair_count == 2


def rank(item):
    counter = {}
    for char in item:
        counter.setdefault(char, 0)
        counter[char] += 1

    # check five

    if is_count(counter, 5):
        return 6

    # check four
    if is_count(counter, 4):
        return 5

    # check house
    if is_count(counter, 3) and is_count(counter, 2):
        return 4

    if is_count(counter, 3):
        return 3

    if is_two_pairs(counter):
        return 2

    if is_count(counter, 2):
        return 1

    return 0


def get_hand_value(item: str):
    return int(
        item.replace("T", "a")
        .replace("J", "b")
        .replace("Q", "c")
        .replace("K", "d")
        .replace("A", "e"),
        16,
    )


def part1():
    input = """32T3K 765
    T55J5 684
    KK677 28
    KTJJT 220
    QQQJA 483"""

    lines = input.split("\n")

    with open("./input.txt") as input_file:
        lines = input_file.readlines()
        lines = [line.strip() for line in lines]

    hands = []
    for line in lines:
        cards, bid = line.split(" ")
        num_bid = int(bid)

        hand_rank = rank(cards)
        hand_value = get_hand_value(cards)

        hands.append((cards, num_bid, hand_rank, hand_value))

    sorted_hands = sorted(hands, key=lambda x: 1000000 * x[2] + x[3])

    bids = [(index + 1) * hand[1] for index, hand in enumerate(sorted_hands)]
    print(sum(bids))


# part 2


def is_count_with_joker(item, count):
    joker_count = 0

    for key in item:
        if key == "J":
            joker_count = item[key]

    return is_count(item, count - joker_count, exclude="J")


def is_two_pairs_with_joker(item):
    joker_count = 0

    for key in item:
        if key == "J":
            joker_count = item[key]

    if joker_count == 1:
        return is_count(item, 2, exclude="J")

    if joker_count == 2:
        return True

    return is_two_pairs(item)


def check_house_with_joker(item):
    item.setdefault("J", 0)
    joker_count = item["J"]

    if joker_count == 2:
        if is_count(item, 2, exclude="J"):
            return True

    if joker_count == 1:
        if is_two_pairs(item):
            return True

    return is_count(item, 3) and is_count(item, 2)


def rank_joker(item):
    counter = {}
    counter["X"] = 0
    for char in item:
        counter.setdefault(char, 0)
        counter[char] += 1

    # check five

    if is_count_with_joker(counter, 5):
        return 6

    # check four
    if is_count_with_joker(counter, 4):
        return 5

    # check house
    if check_house_with_joker(counter):
        return 4

    if is_count_with_joker(counter, 3):
        return 3

    if is_two_pairs_with_joker(counter):
        return 2

    if is_count_with_joker(counter, 2):
        return 1

    return 0


def get_hand_value_joker(item: str):
    return int(
        item.replace("T", "a")
        .replace("J", "0")
        .replace("Q", "c")
        .replace("K", "d")
        .replace("A", "e"),
        16,
    )


def part2():
    input = """32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483"""

    lines = input.split("\n")

    with open("./input.txt") as input_file:
        lines = input_file.readlines()
        lines = [line.strip() for line in lines]

    hands = []
    for line in lines:
        cards, bid = line.split(" ")
        num_bid = int(bid)

        hand_rank = rank_joker(cards)
        hand_value = get_hand_value_joker(cards)

        hands.append((cards, num_bid, hand_rank, hand_value))

    sorted_hands = sorted(hands, key=lambda x: 1000000 * x[2] + x[3])

    print(sorted_hands)

    bids = [(index + 1) * hand[1] for index, hand in enumerate(sorted_hands)]
    print(sum(bids))


part2()
