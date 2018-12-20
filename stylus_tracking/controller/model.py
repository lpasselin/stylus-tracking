class AppModel:
    def __init__(self):
        self.current_frame = None
        self.graph = None
        self.new_x = None
        self.new_y = None
        self.new_z = None
        self.x = []
        self.y = []
        self.z = []

    def add_point(self, point):
        real = self.__from_homogeneous_to_real(point)
        self.x.append(real[0])
        self.y.append(real[1])
        self.z.append(real[2])
        self.new_x = real[0]
        self.new_y = real[1]
        self.new_z = real[2]


    def __from_homogeneous_to_real(self, point):
        return [point[0] / point[3], point[1] / point[3], point[2] / point[3]]

    def reset_graph(self):
        self.x = []
        self.y = []
        self.z = []
