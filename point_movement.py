from objects import Point
import numpy as np
from math import isclose
from numba import njit


def get_rotation_matrix(axis: str, radians: float) -> np.ndarray:
    if axis == "x":
        rotation_matrix = np.array(
            [
                [1, 0, 0],
                [0, np.cos(radians), -np.sin(radians)],
                [0, np.sin(radians), np.cos(radians)],
            ]
        )
    elif axis == "y":
        rotation_matrix = np.array(
            [
                [np.cos(radians), 0, np.sin(radians)],
                [0, 1, 0],
                [-np.sin(radians), 0, np.cos(radians)],
            ]
        )
    elif axis == "z":
        rotation_matrix = np.array(
            [
                [np.cos(radians), -np.sin(radians), 0],
                [np.sin(radians), np.cos(radians), 0],
                [0, 0, 1],
            ]
        )
    else:
        raise ValueError(f"Invalid axis '{axis}'. Axis must be 'x', 'y', or 'z'.")

    return rotation_matrix


def intersect_2d_lines(line1, line2):
    x1, y1 = line1.point1.x, line1.point1.y
    x2, y2 = line1.point2.x, line1.point2.y
    x3, y3 = line2.point1.x, line2.point1.y
    x4, y4 = line2.point2.x, line2.point2.y

    # calculate the denominator
    denom = (y4 - y3) * (x2 - x1) - (x4 - x3) * (y2 - y1)
    if isclose(denom, 0.0, rel_tol=1e-9):
        # lines are parallel or coincident
        return None

    # calculate the point of intersection
    t1 = (x4 - x3) * (y1 - y3) - (y4 - y3) * (x1 - x3)
    t2 = (x2 - x1) * (y1 - y3) - (y2 - y1) * (x1 - x3)
    t = t1 / denom
    u = -t2 / denom
    if not 0 <= t <= 1 or not 0 <= u <= 1:
        # intersection point is outside the line segments
        return None

    x = x1 + t * (x2 - x1)
    y = y1 + t * (y2 - y1)
    return Point(x, y)


def distance(point1, point2):
    return np.sqrt(
        (point1.x - point2.x) ** 2
        + (point1.y - point2.y) ** 2
        + (point1.z - point2.z) ** 2
    )


def scale_points(points, scale_factor, center_point):
    scaled_points = []
    for point in points:
        dx = point.x - center_point.x
        dy = point.y - center_point.y
        dz = point.z - center_point.z

        scaled_x = center_point.x + dx * scale_factor
        scaled_y = center_point.y + dy * scale_factor
        scaled_z = center_point.z + dz * scale_factor

        scaled_points.append(Point(scaled_x, scaled_y, scaled_z))
    return scaled_points


def translate(point, x, y, z):
    return Point(point.x + x, point.y + y, point.z + z)


def rotate_x(point, origin, degrees):
    radians = np.radians(degrees)

    # Translation to the origin
    translated_point = point - origin

    # Rotation matrix
    rotation_matrix = np.array(
        [
            [1, 0, 0],
            [0, np.cos(radians), -np.sin(radians)],
            [0, np.sin(radians), np.cos(radians)],
        ]
    )

    # Rotate point
    rotated_point = np.dot(rotation_matrix, translated_point.a)

    # Translate back to original position
    return Point(rotated_point[0], rotated_point[1], rotated_point[2]) + origin


def rotate_y(point, origin, degrees):
    radians = np.radians(degrees)

    # Translation to the origin
    translated_point = point - origin

    # Rotation matrix
    rotation_matrix = np.array(
        [
            [np.cos(radians), 0, np.sin(radians)],
            [0, 1, 0],
            [-np.sin(radians), 0, np.cos(radians)],
        ]
    )

    # Rotate point
    rotated_point = np.dot(rotation_matrix, translated_point.a)

    # Translate back to original position
    return Point(rotated_point[0], rotated_point[1], rotated_point[2]) + origin


def rotate_z(point, origin, degrees):
    radians = np.radians(degrees)

    # Translation to the origin
    translated_point = point - origin

    # Rotation matrix
    rotation_matrix = np.array(
        [
            [np.cos(radians), -np.sin(radians), 0],
            [np.sin(radians), np.cos(radians), 0],
            [0, 0, 1],
        ]
    )

    # Rotate point
    rotated_point = np.dot(rotation_matrix, translated_point.a)

    # Translate back to original position
    return Point(rotated_point[0], rotated_point[1], rotated_point[2]) + origin


@njit
def rotate(rotation_matrix, rotated_points):
    return [
        [*(np.dot(rotation_matrix, np.array([p[0], p[1], p[2]])))]
        for p in rotated_points
    ]


def rotate_multi(points, origin, angles):
    """
    Rotate multiple points around the origin
    :param points: The list of points to be rotated.
    :param origin: The origin point.
    :param angles: (Tuple[float, float, float]): The rotation angles around x, y, and z axes in degrees.
    :return: list[Point]: The rotated points.
    """
    radians = [np.radians(angle) for angle in angles]
    axes = ["x", "y", "z"]
    rotation_matrices = [
        get_rotation_matrix(axis, radians[i]) if radians[i] != 0 else np.eye(3)
        for i, axis in enumerate(axes)
    ]

    # Translation to the origin for all points
    translated_points = [p - origin for p in points]

    # convert points to numpy array
    rotated_points = np.array([p.a for p in translated_points])
    for i, axis in enumerate(axes):
        if radians[i] != 0:
            rotation_matrix = rotation_matrices[i]
            rotated_points = rotate(rotation_matrix, rotated_points)
            # convert lists in rotated_points to point objects
            rotated_points = [Point(*p) for p in rotated_points]

    # Translate back to original position
    results = [p + origin for p in rotated_points]

    return results
