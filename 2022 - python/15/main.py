import re

input = """Sensor at x=2, y=18: closest beacon is at x=-2, y=15
Sensor at x=9, y=16: closest beacon is at x=10, y=16
Sensor at x=13, y=2: closest beacon is at x=15, y=3
Sensor at x=12, y=14: closest beacon is at x=10, y=16
Sensor at x=10, y=20: closest beacon is at x=10, y=16
Sensor at x=14, y=17: closest beacon is at x=10, y=16
Sensor at x=8, y=7: closest beacon is at x=2, y=10
Sensor at x=2, y=0: closest beacon is at x=2, y=10
Sensor at x=0, y=11: closest beacon is at x=2, y=10
Sensor at x=20, y=14: closest beacon is at x=25, y=17
Sensor at x=17, y=20: closest beacon is at x=21, y=22
Sensor at x=16, y=7: closest beacon is at x=15, y=3
Sensor at x=14, y=3: closest beacon is at x=15, y=3
Sensor at x=20, y=1: closest beacon is at x=15, y=3"""


with open("input.txt") as file_input:
    input = file_input.read()


beacon_mask = set()
beacons = set()
sensors = set()


row_to_check = 2000000


lines = input.split("\n")
for line in lines:
    matches = re.match(
        "Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)", line)
    [sensor_x, sensor_y, beacon_x, beacon_y] = [
        int(group) for group in matches.groups()]
    sensors.add((sensor_x, sensor_y))
    beacons.add((beacon_x, beacon_y))

    distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)

    # sensor to row_to_check delta
    # rest left and right

    distance_to_row = abs(row_to_check - sensor_y)
    delta = distance - distance_to_row
    if delta >= 0:
        points = [(sensor_x, row_to_check)]
        for x in range(1, delta + 1):
            points.append((points[0][0] + x, row_to_check))
            points.append((points[0][0] - x, row_to_check))

        for point in points:
            beacon_mask.add(point)

beacon_list = [item[0]
               for item in beacon_mask if item not in beacons and item not in sensors]
beacon_list.sort()
print(len(beacon_list))


# part 2

# line = [(0,0,4000000)]


x_max = 4000000
y_max = 4000000


matrix = [[(0, x_max)] for _ in range(y_max)]

lines = input.split("\n")


sensor_distances = []
for line in lines:
    matches = re.match(
        "Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)", line)
    [sensor_x, sensor_y, beacon_x, beacon_y] = [
        int(group) for group in matches.groups()]
    distance = abs(beacon_x - sensor_x) + abs(beacon_y - sensor_y)
    sensor_distances.append((sensor_x, sensor_y, distance))


intersection_points = {}
sensor_lines = []
# each sensor has 4 lines y=x + strength, y = x-strength, y=-x + strength y = -x - strength
# each sensor against each sensor, find intersections of all other lines
# if intersection point within area and not too close to any other sensor, add to intersection points
# if found, break, give answer

for sensor_x, sensor_y, strength in sensor_distances:
    strength += 1

    for other_x, other_y, other_strength in sensor_distances:
        other_strength += 1
