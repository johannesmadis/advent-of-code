import re
import math
rules_input = [line.split(": ")
               for line in open("16.rules.txt").read().split("\n")]
tickets_input = [[int(item) for item in line.split(",")]
                 for line in open("16.tickets.txt").read().split("\n")]
personal_ticket = [int(item) for item in open(
    "16.personal-ticket.txt").read().split(",")]

"""
print("rules", rules)
print("tickets", tickets)
print("personal_ticket", personal_ticket)
"""


class Range:
    def __init__(self, min, max):
        self.min = min
        self.max = max

    def test(self, value):
        return value >= self.min and value <= self.max


class Rule:
    def __init__(self, name: str, range0, range1):
        self.name = name
        self.range0 = range0
        self.range1 = range1
        self.index = -1

    def test(self, value: int) -> bool:
        return self.range0.test(value) or self.range1.test(value)

    def set_index(self, index):
        self.index = index


class Ticket:
    def __init__(self, values):
        self.values = values
        self.valid = True

    def validate_single(self, field, rules):
        # ticket validates single rule if any of values
        current_valid = False
        for rule in rules:
            valid = rule.test(field)
            if valid is True:
                current_valid = valid
                break
        return current_valid

    def validate(self, rules):
        # ticket is valid if all fields are within given rules
        current_valid = True

        for field in self.values:
            current_valid = self.validate_single(field, rules)
            if current_valid is False:
                break

        self.valid = current_valid


ticket_personal = Ticket(personal_ticket)


rules = []
for rule_input in rules_input:
    rule_name = rule_input[0]
    value_ranges = rule_input[1].split(" or ")

    range0 = [int(item) for item in value_ranges[0].split("-")]
    range1 = [int(item) for item in value_ranges[1].split("-")]

    rules.append(Rule(rule_name, Range(
        range0[0], range0[1]), Range(range1[0], range1[1])))


# create tickets
tickets = []

for ticket in tickets_input:
    tickets.append(Ticket(ticket))

# validate tickets
valid_tickets = [ticket_personal]
for ticket in tickets:
    ticket.validate(rules)
    if ticket.valid is True:
        valid_tickets.append(ticket)

# find rule indices by fields
while (sum([int(rule.index != -1) for rule in rules]) != len(rules)):
    for index in range(len(rules)):
        # find which rule this index belongs to
        # by finding which rule is valid for all tickets
        tickets_fields = [ticket.values[index] for ticket in valid_tickets]
        found = False
        valid_rules = []
        for rule in rules:
            if (rule.index != -1):
                continue
            valid_for_index = [int(rule.test(field))
                               for field in tickets_fields]
            if (sum(valid_for_index) == len(tickets_fields)):
                valid_rules.append(rule)

        if len(valid_rules) == 1:
            rule = valid_rules[0]
            rule.set_index(index)

print([[rule.name, rule.index] for rule in rules])


"""
for rule in rules:
    # find field index for which all tickets validate against this rule
    for index in range(len(rules)):
        rule.test_index(index, valid_tickets)
"""


departure = (12, 7, 13, 17, 1, 4)
print(math.prod([ticket_personal.values[index] for index in departure]))


"""

error_rate = 0


new_tickets = [personal_ticket]
for ticket in tickets_input:
    ticket_valid = True

    for field in ticket:
        valid = False
        for rule in rules:
            for rule_range in rule["ranges"]:
                if (field >= rule_range["min"] and field <= rule_range["max"]):
                    valid = True
                    # found valid range within rule, can break
                    break
            if valid is True:
                # found valid rule, can break
                break
        if (valid is False):
            ticket_valid = False
            error_rate += field

    if (ticket_valid is True):
        new_tickets.append(ticket)


print(len(tickets_input), len(new_tickets))

# find rule index
# first index that all neighbor tickets are ok


rule_indices = {}
for rule in rules:
    name = rule["name"]
    rule_index = -1
    for field_index in range(20):  # field count
        valid = True
        for ticket in new_tickets:
            field = ticket[field_index]
            in_ranges = False

            for rule_range in rule["ranges"]:
                if (field >= rule_range["min"] and field <= rule_range["max"]):
                    in_ranges = True
                    break
            # print(field_index, field, rule["ranges"])
            if in_ranges is False:
                valid = False
                break
        if valid is True:
            rule_index = field_index

    rule_indices[name] = rule_index

print(rule_indices)
"""
