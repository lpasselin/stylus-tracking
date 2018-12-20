import numpy as np


class AppModel:
    SCALER = 4
    X = 103 * SCALER
    Y = 135 * SCALER
    Z = 256

    def __init__(self):
        self.current_frame = None
        self.graph = None
        self.new_x = None
        self.new_y = None
        self.new_z = None
        self.x = []
        self.y = []
        self.z = []
        self.drawing = np.zeros([self.X * 2 + 2, self.Y * 2 + 2, 3], dtype=np.uint8)

    def add_point(self, point):
        real = self.__from_homogeneous_to_real(point)
        self.x.append(real[0])
        self.y.append(real[1])
        self.z.append(real[2])
        self.new_x = real[0]
        self.new_y = real[1]
        self.new_z = real[2]

        self.update_drawing(real)

    def update_drawing(self, p):
        x, y, z = p
        x *= self.SCALER
        y *= self.SCALER
        if x < -self.X or x > self.X:
            return
        elif y < -self.Y or y > self.Y:
            return
        elif z < -self.Z or z > self.Z:
            return

        ix = int(x) + self.X
        iy = int(y) + self.Y
        iz = 256 - abs(int(z))

        self.drawing[ix, iy, 0] = iz
        self.drawing[ix, iy, 1] = iz
        self.drawing[ix, iy, 2] = iz

    def __from_homogeneous_to_real(self, point):
        return [point[0] / point[3], point[1] / point[3], point[2] / point[3]]

    def reset_graph(self):
        self.x = []
        self.y = []
        self.z = []
