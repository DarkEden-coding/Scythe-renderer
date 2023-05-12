import numpy as np


class Point:
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.t = (self.x, self.y)
        self.a = np.array([self.x, self.y, self.z])

    def update(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.t = (self.x, self.y)
        self.a = np.array([self.x, self.y, self.z])

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Point(self.x - other.x, self.y - other.y, self.z - other.z)

    def __str__(self):
        return f"Point({self.x}, {self.y}, {self.z})"


class Line3D:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def update(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def get_midpoint(self):
        return Point(
            (self.point1.x + self.point2.x) / 2,
            (self.point1.y + self.point2.y) / 2,
            (self.point1.z + self.point2.z) / 2,
        )

    def get_2d_line_xy(self):
        return Line2D(
            Point(self.point1.x, self.point1.y), Point(self.point2.x, self.point2.y)
        )

    def get_2d_line_xz(self):
        return Line2D(
            Point(self.point1.x, self.point1.z), Point(self.point2.x, self.point2.z)
        )

    def get_2d_line_yz(self):
        return Line2D(
            Point(self.point1.y, self.point1.z), Point(self.point2.y, self.point2.z)
        )

    def __str__(self):
        return f"Line3D({str(self.point1)}, {str(self.point2)})"


class Line2D:
    def __init__(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def update(self, point1, point2):
        self.point1 = point1
        self.point2 = point2

    def get_slope(self):
        return (self.point2.y - self.point1.y) / (self.point2.x - self.point1.x)

    def get_midpoint(self):
        return Point(
            (self.point1.x + self.point2.x) / 2, (self.point1.y + self.point2.y) / 2
        )

    def __str__(self):
        return f"Line2D({str(self.point1)}, {str(self.point2)})"


class Face:
    def __init__(self, vertices):
        self.vertices = vertices

    def center(self):
        x_sum, y_sum, z_sum = 0, 0, 0
        for vertex in self.vertices:
            x_sum += vertex.x
            y_sum += vertex.y
            z_sum += vertex.z
        n = len(self.vertices)
        return Point(x_sum / n, y_sum / n, z_sum / n)

    def update(self, vertices):
        self.vertices = vertices
