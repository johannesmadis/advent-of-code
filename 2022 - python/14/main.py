input = """498,4 -> 498,6 -> 496,6
503,4 -> 502,4 -> 502,9 -> 494,9"""


class Polyline:
    def __init__(self, corners):
        self.corners = corners

        print("corners", self.corners)
        self.points = set()
        for i in range(len(corners)):
            start = corners[i]

            if len(corners) == i+1:
                self.points.add(start)
                continue

            end = corners[i+1]
            print(start.real, end.real)
            for middle_x in range(int(start.real), int(end.real)):
                print("middlex", middle_x)
                self.points.add(complex(middle_x, start.imag))

            for middle_y in range(int(start.imag), int(end.imag)):
                print("middley", middle_y)
                self.points.add(complex(start.real, middle_y))

    def __repr__(self):
        return f"Polyline {self.points}"


polylines = []

for line in input.split("\n"):
    points_str = [point.split(",") for point in line.split(" -> ")]
    points = [complex(int(x), int(y)) for [x, y] in points_str]
    polylines.append(Polyline(points))

print(polylines)
