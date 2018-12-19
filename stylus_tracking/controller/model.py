def __from_homogeneous_to_real(point):
    return [point[0] / point[3], point[1] / point[3], point[2] / point[3]]


class AppModel:
    def __init__(self):
        self.current_frame = None
        self.graph = None
        self.points = []
        self.x = []
        self.y = []
        self.z = []

    def add_point(self, point):
        real = __from_homogeneous_to_real(point)
        self.x.append(real[0])
        self.y.append(real[1])
        self.z.append(real[2])
