import pygame
from objects import Point
from settings import (
    width,
    height,
    focal_length,
    draw_verts,
    draw_lines,
    vert_color,
    line_color,
    vert_size,
    line_width,
)
from point_movement import rotate_multi
from numba import njit


@njit
def get_point(
    input_point_x,
    input_point_y,
    input_point_z,
    camera_vanishing_point_x,
    camera_vanishing_point_y,
    camera_vanishing_point_z,
):
    try:
        x = (
            (input_point_x - camera_vanishing_point_x)
            * focal_length
            / (input_point_y - camera_vanishing_point_y)
        )
        y = (
            (input_point_z - camera_vanishing_point_z)
            * focal_length
            / (input_point_y - camera_vanishing_point_y)
        )
    except:
        return width / 2, height / 2, True
    # if input point is behind the camera, return None
    if input_point_y < camera_vanishing_point_y:
        return x + width / 2, y + height / 2, False
    if x > width or x < -width:
        return x + width / 2, y + height / 2, False
    if y > height or y < -height:
        return x + width / 2, y + height / 2, False
    return x + width / 2, y + height / 2, True


def draw_object(points, lines, screen, camera):
    flat_points = []

    if camera.rotation_z != 0:
        points = rotate_multi(points, camera.vanishing_point, (0, 0, camera.rotation_z))
    if camera.rotation_x != 0:
        points = rotate_multi(points, camera.vanishing_point, (camera.rotation_x, 0, 0))

    def draw_point(point):
        x, y, draw = get_point(
            point.x,
            point.y,
            point.z,
            camera.vanishing_point.x,
            camera.vanishing_point.y,
            camera.vanishing_point.z,
        )
        flat_point = Point(x, y)
        flat_points.append({"point": flat_point, "draw": draw})
        if draw and draw_verts:
            pygame.draw.circle(screen, vert_color, flat_point.t, vert_size, 0)

    for point in points:
        draw_point(point)

    for line in lines:
        if line[0] >= len(flat_points) or line[1] >= len(flat_points):
            continue
        start_pos = flat_points[line[0]].get("point")
        end_pos = flat_points[line[1]].get("point")
        if (
            start_pos is not None
            and end_pos is not None
            and flat_points[line[0]].get("draw")
            and flat_points[line[1]].get("draw")
            and draw_lines
        ):
            pygame.draw.line(screen, line_color, start_pos.t, end_pos.t, line_width)
