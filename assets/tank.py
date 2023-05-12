import sys

sys.path.append("..")

from point_movement import (
    translate,
    rotate_multi,
)
from objects import Point


def center_point(points):
    # Initialize the sum of all the points
    sum_x, sum_y, sum_z = 0, 0, 0

    # Iterate over all the points in the list and add their values
    for point in points:
        sum_x += point.x
        sum_y += point.y
        sum_z += point.z

    # Calculate the average of each coordinate
    avg_x = sum_x / len(points)
    avg_y = sum_y / len(points)
    avg_z = sum_z / len(points)

    # Return a new point object with the average coordinates
    return Point(avg_x, avg_y, avg_z)


class Tank:
    def __init__(self):
        points = []
        lines = []
        with open("assets/t-90.obj", "r") as f:
            data = f.read()
        for line in data.splitlines():
            tmp = []
            if line.startswith("v "):
                for vert in line.strip("v  ").split(" "):
                    tmp.append(vert)
                points.append(
                    Point(float(tmp[0]) * 10, float(tmp[1]) * 10, float(tmp[2]) * 10)
                )
            elif line.startswith("f "):
                # Split the line into its components and convert them to integers
                components = line.split()[1:]
                indices = [int(c.split("/")[0]) - 1 for c in components]
                i1, i2 = indices[0], indices[1]
                lines.append((i1, i2))
        self.verticies = points
        self.lines = lines

    def move(self, x, y, z):
        for i, vert in enumerate(self.verticies):
            self.verticies[i] = translate(self.verticies[i], x, y, z)

    def rotate(self, x, y, z):
        self.verticies = rotate_multi(
            self.verticies, center_point(self.verticies), (x, y, z)
        )
