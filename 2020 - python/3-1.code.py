class Map():
    def __init__(self, inputs):
        self.inputs = inputs

        self.slopes = ((1, 1), (3, 1), (5, 1), (7, 1), (1, 2))

    def count_trees_for_slope(self, right, down):
        tree_count = 0

        for index in range(0, len(self.inputs), down):
            line = self.inputs[index]
            line_index = int((index * right / down) % len(line))
            if (line[line_index] == "#"):
                tree_count += 1

        return tree_count

    def count_trees(self):

        # for each line, the index is
        result = 1

        for slope in self.slopes:
            right = slope[0]
            down = slope[1]
            slope_result = self.count_trees_for_slope(right, down)
            print(slope_result)
            result = result * slope_result

        return result


with open("3-1.input.txt") as f:
    inputs = f.read().split("\n")

    trajectory = Map(inputs)
    tree_count = trajectory.count_trees()
    print(tree_count)
