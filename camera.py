from objects import Point


class Camera:
    def __init__(self, vanishing_point=Point(0, 0, 0), rotation_x=0, rotation_y=0, rotation_z=0):
        """
        defines the camera object, points are defined in the following order:
        1: top right
        2: bottom right
        3: top left
        4: bottom left
        :param vanishing_point: Point behind the camera plane, rotation is done around this point
        :param rotation_x: rotation around the local x-axis
        :param rotation_y: rotation around the local y-axis
        :param rotation_z: rotation around the local z-axis
        """
        self.vanishing_point = vanishing_point
        self.rotation_x = rotation_x
        self.rotation_y = rotation_y
        self.rotation_z = rotation_z

    # soh cah toa
    def move(self, x, y, z):
        self.vanishing_point.update(
            self.vanishing_point.x + x,
            self.vanishing_point.y + y,
            self.vanishing_point.z + z,
        )

    def rotate(self, x, y, z):
        self.rotation_x += x
        self.rotation_z += z
        self.rotation_y += y
