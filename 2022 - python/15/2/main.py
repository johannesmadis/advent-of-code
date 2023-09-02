import re
from typing import Dict

def manhattan(a: complex,b: complex):
    return abs(a.real-b.real) + abs(a.imag-b.imag)

LIMIT = 4000000


def intersect_lines(up:complex, down:complex):
    x = (down.real - up.real) / 2 + down.real
    y = (down.real - up.real) / 2
    return complex(x,y)

class Sensor:
    def __init__(self, sx,sy,bx,by):
        self.x = sx
        self.y = sy
        self.beacon = complex(bx,by)
        self.coords = complex(sx,sy)
        self.radius = int(manhattan(self.beacon,self.coords))

    def __repr__(self):
        return f"Sensor ({self.coords},{self.beacon},{self.radius})"
    
    def get_lines(self):
        # line represented by slope (1 or -1) and x if y is 0
        # (x, slope)
        line0 = complex(self.y - self.radius-1 - self.x,-1)   #/
        line1 = complex(self.y + self.radius+1  + self.x,1)   #\
        line2 = complex(self.y + self.radius+1 - self.x ,-1)    #/
        line3 = complex(self.y - self.radius-1 + self.x ,1)   #\

        return (line0, line1, line2, line3)

    


    

input_data = ""
with open("./input.txt") as input_file:
    input_data = input_file.readlines()

#read lines with regex

sensors = []
for line in input_data:
    matches = re.match("Sensor at x=([\-\d]+), y=([\-\d]+): closest beacon is at x=([\-\d]+), y=([\-\d]+)", line)
    [sx,sy,bx,by] = [int(group) for group in matches.groups()]

    sensors.append(Sensor(sx,sy,bx,by))

print("Sensors", len(sensors))

perimeter_lines = {}
for sensor in sensors:
    lines = sensor.get_lines()
    for line in lines:
        perimeter_lines.setdefault(line,0)
        perimeter_lines[line] += 1

lines_up = []
lines_down  = []
for line in perimeter_lines:
    count = perimeter_lines[line]
    if count > 1:
        if line.imag > 0:
            lines_up.append(line)
        else:
             lines_down.append(line)

print("lines up", lines_up)
print("lines down", lines_down)

intersections = []
for up in lines_up:
    for down in lines_down:
        intersection = intersect_lines(up, down)
        if (intersection.imag <= LIMIT and intersection.real <= LIMIT):
            intersections.append(intersection)

print("intersections",[intersection for intersection in intersections if intersection.real <= LIMIT and intersection.imag <= LIMIT and intersection.real >= 0 and intersection.imag >= 0])