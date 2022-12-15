import re
# record children
# recursive look into each to see if it will end up with gold

child_pattern = r"(\d+) (\b.+\b \b.+\b) bags?"
graph = {}
items = []

with open("7-1.input.txt") as f:
    lines = f.readlines()

    for line in lines:
        relations = line.split(" contain ")
        parent = relations[0]
        children = relations[1].split(", ")

        parent_items = parent.split(" ")
        formatted_parent = (parent_items[0] + " " + parent_items[1])
        items.append(formatted_parent)

        graph[formatted_parent] = {"name": formatted_parent, "children": {}}

        for child in children:
            child_items = child.strip().split(" ")
            # if length is 4, then it is valid, otherwise it's "no other bags."
            if (len(child_items) == 4):
                count = int(child_items[0])
                formatted_child = child_items[1] + " " + child_items[2]
                graph[formatted_parent]["children"][formatted_child] = {
                    "count": count, "name": formatted_child}


root = "shiny gold"


def find_parents(node, parents):
    # if no more parents, increment counter
    for item in items:
        graph_item = graph[item]
        if (node in graph_item["children"]):
            # current graph is direct parent
            parents[item] = True
            # find parents for current items as well
            find_parents(item, parents)


parents = {}

find_parents(root, parents)


def find_children(node, children, counter):
    current_node = graph[node]
    for child in current_node["children"]:
        child_item = current_node["children"][child]
        if (child in children):
            children[child] += counter * child_item["count"]
        else:
            children[child] = counter * child_item["count"]
        find_children(child, children, counter * child_item["count"])


children = {}
find_children(root, children, 1)

final = 0
for child in children:
    final += children[child]

print(final)

# print(len(parents))
