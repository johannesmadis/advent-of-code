

"""

class Sign:
    def __init__(self,a,b):
        self.us = b
        self.them = a

class SIGN:
    ROCK = Sign("A","X")
    PAPER = Sign("B","Y")
    SCISSORS = Sign("C","Z")

class Party:
    def __init__(self,rock,paper,scissors):
        self.rock = rock
        self.paper = paper
        self.scissors = scissors

US = Party("X","Y", "Z")
THEM = Party("A","B", "C")


def play(them, us):

    if us == US.rock:
        if them == THEM.rock:
            return SCORE.ROCK + SCORE.DRAW
        elif them == THEM.paper: 
            return SCORE.ROCK + SCORE.LOSE
        else:   # scissors
            return SCORE.ROCK + SCORE.WIN
            
    elif us == US.paper:
        if them == THEM.rock:
            return SCORE.PAPER + SCORE.WIN
        elif them == THEM.paper: 
            return SCORE.PAPER + SCORE.DRAW
        else:   
            return SCORE.PAPER + SCORE.LOSE
    else: # scissors
        if them == THEM.rock:
            return SCORE.SCISSORS + SCORE.LOSE
        elif them == THEM.paper: 
            return SCORE.SCISSORS + SCORE.WIN
        else:   
            return SCORE.SCISSORS + SCORE.DRAW



def part1(input):
    total = 0
    for line in input:
        items = line.split(" ")
        result = play(items[0].strip(), items[1].strip())
        total += result
    print(total)
"""
class SCORE:
    LOSE = 0
    DRAW = 3
    WIN = 6
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

signs = {
    "A": { #rock
        "X": "C", #wins scissors
        "Y": "A", # draw
        "Z": "B", # loses paper
        "_S": 1
    },
    "B": { #paper
        "X": "A", #win rock
        "Y": "B", # draw
        "Z": "C", # loses 
        "_S": 2
    },
    "C": { #scissors
        "X": "B", #wins paper
        "Y": "C", # draw
        "Z": "A", # loses
        "_S": 3
    }
}

results_scores = {
    "X": 0,
    "Y": 3,
    "Z": 6
}


def part2(input_lines):
    total = 0
    for line in input_lines:
        [them,result] = [x.strip() for x in line.split(" ")]
        us = signs[them][result]

        score = results_scores[result] + signs[us]["_S"]
        total += score
    print(total)

with open("C:/Users/kasutaja7yh/Desktop/aoc-2022/02/input.txt") as input:
    part2(input.readlines())