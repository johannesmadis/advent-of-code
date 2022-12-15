import copy
content = open("19.input.txt").read().split("\n\n")

rules = content[0].split("\n")
text = content[1].split("\n")

"""
0: a
1: b
2: a|b
"""


rule_map = {}
for rule in rules:
    items = rule.split(": ")

    conditions = items[1].split(" | ")

    rule_map[int(items[0])] = [item.replace('"', "").split(" ")
                               for item in conditions]


for rule in rule_map:
    print(rule, rule_map[rule])

valid_strings_by_rule = []


def replace_rule(start, rule_map):
    for optionI, option in enumerate(start):
        for ruleI, rule_index in enumerate(option):
            if rule_index != "a" and rule_index != "b":
                int_rule_index = int(rule_index)
                start[optionI][ruleI] = replace_rule(
                    copy.deepcopy(rule_map[int_rule_index]), rule_map)
    return start


replaced = replace_rule(copy.deepcopy(rule_map[0]), rule_map)

# def parse(str, rule):


print(replaced)
# for each optional substitute numbers with rule by that number until no numbers left
