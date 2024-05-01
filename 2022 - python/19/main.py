import re
from queue import Queue

CLAY = "clay"
OBSIDIAN = "obsidian"
GEODE = "geode"
ORE = "ore"

RESOURCES = "resources"
ROBOTS = "robots"
ROUNDS_LEFT = "rounds_left"


def parse_blueprint(line: str):
    matches = re.match(
        ".+?(\d+) ore.+?(\d+) ore.+?(\d+) ore.+?(\d+) clay.+?(\d+) ore.+?(\d+) obsidian",
        line,
    )
    (
        ore_ore,
        clay_ore,
        obsidian_ore,
        obsidian_clay,
        geode_ore,
        geode_obsidian,
    ) = matches.groups()
    return {
        ORE: {ORE: int(ore_ore)},
        CLAY: {ORE: int(clay_ore)},
        OBSIDIAN: {ORE: int(obsidian_ore), CLAY: int(obsidian_clay)},
        GEODE: {ORE: int(geode_ore), OBSIDIAN: int(geode_obsidian)},
    }


def action_wait(state):
    new_state = clone_state(state)
    increment_resources(new_state)
    new_state[ROUNDS_LEFT] -= 1

    return new_state


def build_robot(state, robot, robot_blueprint):
    new_state = action_wait(state)
    new_state[ROBOTS][robot] += 1
    for resource in robot_blueprint:
        new_state[RESOURCES][resource] -= robot_blueprint[resource]

    return new_state


def increment_resources(state):
    for robot in state[ROBOTS]:
        robot_count = state[ROBOTS][robot]
        state[RESOURCES][robot] += robot_count

    return state


def clone_state(state):
    new_state = {
        RESOURCES: state[RESOURCES].copy(),
        ROBOTS: state[ROBOTS].copy(),
        ROUNDS_LEFT: state[ROUNDS_LEFT],
    }
    return new_state


def main():
    with open("input.test.txt") as f:
        lines = f.readlines()
        blueprints = [parse_blueprint(line) for line in lines]
        print(blueprints)

    state = {
        RESOURCES: {ORE: 0, OBSIDIAN: 0, GEODE: 0, CLAY: 0},
        ROBOTS: {ORE: 1, OBSIDIAN: 0, GEODE: 0, CLAY: 0},
        ROUNDS_LEFT: 24,
    }

    result = {}

    for index, blueprint in enumerate(blueprints):
        queue = Queue()

        queue.put(action_wait(state))

        total_geode = 0

        while not queue.empty():
            current_state = queue.get()

            total_geode = max([current_state[RESOURCES][GEODE], total_geode])

            if current_state[ROUNDS_LEFT] != 0:
                queue.put(action_wait(current_state))

                for robot in blueprint:
                    can_afford = True
                    for resource in blueprint[robot]:
                        if blueprint[robot][resource] <= state[RESOURCES][resource]:
                            can_afford = False
                            break

                    if can_afford:
                        queue.put(build_robot(current_state, robot, blueprint[robot]))
        result[index] = total_geode

    print(result)


main()
