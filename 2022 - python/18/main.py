from typing import Dict, Set


def get_unique_faces_count(list_of_tuples):
    faces = {"xy": {}, "xz": {}, "yz": {}}

    for voxel in list_of_tuples:
        x, y, z = voxel
        # front
        faces["xz"].setdefault((x, y, z), 0)
        faces["xz"][(x, y, z)] += 1

        # back
        faces["xz"].setdefault((x, y + 1, z), 0)
        faces["xz"][(x, y + 1, z)] += 1

        # bottom
        faces["xy"].setdefault((x, y, z), 0)
        faces["xy"][(x, y, z)] += 1

        # top
        faces["xy"].setdefault((x, y, z + 1), 0)
        faces["xy"][(x, y, z + 1)] += 1

        # left
        faces["yz"].setdefault((x, y, z), 0)
        faces["yz"][(x, y, z)] += 1

        # right
        faces["yz"].setdefault((x + 1, y, z), 0)
        faces["yz"][(x + 1, y, z)] += 1

    total = 0
    for face_dir in faces:
        face_collection = faces[face_dir]
        for coord in face_collection:
            total += 1 if face_collection[coord] == 1 else 0

    return total


with open("input.test.txt") as f:
    voxel_coords = f.readlines()
    voxel_coord_tuples = [
        [int(coord) for coord in voxel.split(",")] for voxel in voxel_coords
    ]
    print(voxel_coord_tuples)

    total = get_unique_faces_count(voxel_coord_tuples)

    # each coord is in bottom left front corner.
    # so it defines 6 faces, each face has different plane xy,xz,yz
    # count number of faces which are defined only once

    print("part1", total)


def get_neighbors(current, queue, grid: Dict, mist: Set):
    top = (current[0], current[1], current[2] + 1)
    bottom = (current[0], current[1], current[2] - 1)
    left = (current[0] - 1, current[1], current[2])
    right = (current[0] + 1, current[1], current[2])
    front = (current[0], current[1] - 1, current[2])
    back = (current[0], current[1] + 1, current[2])

    for item in (top, bottom, left, right, front, back):
        if item in grid and item not in mist and grid[item] == False:
            queue.append(item)
            mist.add(item)


with open("input.test.txt") as f:
    voxel_coords = f.readlines()

    voxel_coord_tuples = []
    for voxel in voxel_coords:
        coords = voxel.split(",")
        coords = [int(coord) for coord in coords]

        voxel_coord_tuples.append((coords[0], coords[1], coords[2]))

    min_x = min(voxel_coord_tuples, key=lambda x: x[0])[0] - 1
    min_y = min(voxel_coord_tuples, key=lambda x: x[1])[1] - 1
    min_z = min(voxel_coord_tuples, key=lambda x: x[2])[2] - 1
    max_x = max(voxel_coord_tuples, key=lambda x: x[0])[0] + 1
    max_y = max(voxel_coord_tuples, key=lambda x: x[1])[1] + 1
    max_z = max(voxel_coord_tuples, key=lambda x: x[2])[2] + 1

    grid = {}
    for x in range(min_x, max_x + 1):
        for y in range(min_y, max_y + 1):
            for z in range(min_z, max_z + 1):
                cell = (x, y, z)
                grid[cell] = True if cell in voxel_coord_tuples else False

    start = (min_x, min_y, min_z)
    neighbors_queue = []
    mist = set()

    get_neighbors(start, neighbors_queue, grid, mist)

    while len(neighbors_queue) > 0:
        current = neighbors_queue.pop()
        get_neighbors(current, neighbors_queue, grid, mist)

    total = get_unique_faces_count(mist)

    x_bounds = max_x - min_x
    y_bounds = max_y - min_y
    z_bounds = max_z - min_z

    print(x_bounds, y_bounds, z_bounds)

    bounds_area = (
        2 * x_bounds * y_bounds + 2 * x_bounds * z_bounds + 2 * y_bounds * z_bounds
    )
    print(total, bounds_area, total - bounds_area)
