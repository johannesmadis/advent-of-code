import re
from pprint import pprint
from typing import List, Dict, Set
from dijkstra import Node, Edge, Graph


"""
    Alternative algorithm

    Make an adjacency map for each node which tells how many steps each other node is away
    Start at AA
    Go to all other closed nodes and turn them on
        .. repeat until all valves are open or 30 minutes have passed
    Each branch tracks its history and score
    Pick branch with best score.

    
"""


def parse():
    lines = []
    with open("input.txt") as input_file:
        lines = input_file.readlines()

    nodes = []
    edges = []
    for line in lines:
        # Valve II has flow rate=0; tunnels lead to valves AA, JJ
        matches = re.match(
            "Valve (.+) has flow rate=(\d+); tunnels* leads* to valves* (.+)", line
        )
        valve_name, flow_rate_str, neighbor_names = matches.groups()
        neighbors = neighbor_names.split(", ")
        flow_rate = int(flow_rate_str)

        node = Node(valve_name)
        node.value = flow_rate
        node_edges = [Edge(valve_name, neighbor, 1) for neighbor in neighbors]
        nodes.append(node)
        edges.extend(node_edges)

    graph = Graph(nodes, edges)
    distances = graph.calculate_distances()

    return graph, distances


def step(graph: Graph, distances, node: Node, score: int, round, opened_valves: Set):
    # go to each other node with value
    # open it, remaining rounds is (current - distance + 1)
    # add remaining rounds * node value to score
    # continue with child node
    node_distances = distances[node.name]

    scores = [(node.name, score)]
    for target_name in graph.nodes:
        new_score = score
        target = graph.nodes[target_name]
        if target.value == 0:
            continue

        if target.name in opened_valves:
            continue

        new_valves = opened_valves.copy()
        new_valves.add(target.name)

        distance_to_target = node_distances[target_name]
        target_round = round - distance_to_target - 1
        if target_round < 0:
            continue
        new_score += target_round * target.value
        result_score = step(
            graph, distances, target, new_score, target_round, new_valves
        )
        scores.append((target.name, result_score))

    sorted_scores = sorted(scores, reverse=True, key=lambda x: x[1])

    return sorted_scores[0][1]


def run(graph: Graph, distances):
    start_node = graph.nodes["AA"]
    score = 0
    rounds = 30
    opened_valves = set()

    result = step(graph, distances, start_node, score, rounds, opened_valves)
    return result


def find_unique_pairs(input_list):
    unique_pairs = set()  # Use a set to store unique pairs

    # Iterate through the list with two nested loops
    for i in range(len(input_list)):
        for j in range(i + 1, len(input_list)):
            pair = (input_list[i], input_list[j])  # Create a pair of elements
            unique_pairs.add(pair)  # Add the pair to the set

    return list(unique_pairs)  # Convert the set back to a list if needed


def step2(
    graph: Graph,
    distances,
    positions: (Node, Node),
    score,
    rounds: (int, int),
    opened_valves,
):
    # new branch starts each time a decision is made to be made by actor0 or actor2

    # three options
    # both decide
    # 0 decides
    # 1 decides

    elephant_rounds, elf_rounds = rounds
    elephant_pos, elf_pos = positions
    scores = [score]
    candidates = [
        graph.nodes[node_name]
        for node_name in graph.nodes
        if node_name not in opened_valves and graph.nodes[node_name].value != 0
    ]

    elephant_distances = distances[elephant_pos.name]
    elf_distances = distances[elf_pos.name]

    if elephant_rounds == elf_rounds:  # both make new decision
        candidate_pairs = find_unique_pairs(candidates)

        for candidate_elephant, candidate_elf in candidate_pairs:
            new_valves = opened_valves.copy()

            new_valves.add(candidate_elephant.name)
            new_valves.add(candidate_elf.name)

            distance_elf = elf_distances[candidate_elf.name]
            distance_elephant = elephant_distances[candidate_elephant.name]

            target_round_elephant = elephant_rounds - distance_elephant - 1
            target_round_elf = elf_rounds - distance_elf - 1

            if target_round_elephant < 0 and target_round_elf < 0:
                continue

            new_score = score
            if target_round_elephant > 0:
                new_score += candidate_elephant.value * target_round_elephant
            if target_round_elf > 0:
                new_score += candidate_elf.value * target_round_elf

            result_score = step2(
                graph,
                distances,
                (candidate_elephant, candidate_elf),
                new_score,
                (target_round_elephant, target_round_elf),
                new_valves,
            )
            scores.append(result_score)
        sorted_scores = sorted(scores, reverse=True)
        return sorted_scores[0]

    elif elephant_rounds > elf_rounds:  # elephant,0 decides
        scores = [score]
        for target in candidates:
            new_valves = opened_valves.copy()
            new_valves.add(target.name)

            new_score = score
            distance_to_target = elephant_distances[target.name]
            target_round = elephant_rounds - distance_to_target - 1
            if target_round <= 0:
                continue
            new_score += target_round * target.value

            result_score = step2(
                graph,
                distances,
                (target, elf_pos),
                new_score,
                (target_round, elf_rounds),
                new_valves,
            )
            scores.append(result_score)
        sorted_scores = sorted(scores, reverse=True)
        return sorted_scores[0]

    else:  # elf,1 decides,
        scores = [score]
        for target in candidates:
            new_valves = opened_valves.copy()
            new_valves.add(target.name)

            new_score = score
            distance_to_target = elf_distances[target.name]
            target_round = elf_rounds - distance_to_target - 1
            if target_round <= 0:
                continue
            new_score += target_round * target.value

            result_score = step2(
                graph,
                distances,
                (elephant_pos, target),
                new_score,
                (elephant_rounds, target_round),
                new_valves,
            )
            scores.append(result_score)
        sorted_scores = sorted(scores, reverse=True)
        return sorted_scores[0]


def part2(graph: Graph, distances):
    start_node = graph.nodes["AA"]
    score = 0
    rounds = (26, 26)
    positions = (start_node, start_node)
    opened_valves = set()

    result = step2(graph, distances, positions, score, rounds, opened_valves)

    return result


def main():
    graph, distances = parse()
    # pprint(distances)

    # part 1
    result = run(graph, distances)
    print(result)

    # part2
    result2 = part2(graph, distances)
    print(result2)


main()
