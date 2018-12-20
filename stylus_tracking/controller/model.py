import numpy as np


def remove_np_duplicates(data):
  # Perform lex sort and get sorted data
  sorted_idx = np.lexsort(data.T)
  sorted_data =  data[sorted_idx,:]

  # Get unique row mask
  row_mask = np.append([True],np.any(np.diff(sorted_data,axis=0),1))

  # Get unique rows
  out = sorted_data[row_mask]
  return out

def get_grid_cells_btw(p1,p2):
  x1,y1 = p1
  x2,y2 = p2
  dx = x2-x1
  dy = y2-y1

  if dx == 0: # will divide by dx later, this will cause err. Catch this case up here
    step = np.sign(dy)
    ys = np.arange(0,dy+step,step)
    xs = np.repeat(x1, ys.shape[0])
  else:
    m = dy/(dx+0.0)
    b = y1 - m * x1

    step = 1.0/(max(abs(dx),abs(dy)))
    xs = np.arange(x1, x2, step * np.sign(x2-x1))
    ys = xs * m + b

  xs = np.rint(xs)
  ys = np.rint(ys)
  pts = np.column_stack((xs,ys))
  pts = remove_np_duplicates(pts)
  return pts.astype(int)

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
        self.last_x = None
        self.last_y = None
        self.last_z = None

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

        self.drawing[ix, iy, :] = iz, iz, iz
        self.drawing[ix, iy + 1, :] = iz, iz, iz
        self.drawing[ix, iy - 1, :] = iz, iz, iz
        self.drawing[ix + 1, iy, :] = iz, iz, iz
        self.drawing[ix - 1, iy, :] = iz, iz, iz

        if self.last_x:
            for i in get_grid_cells_btw((self.last_x, self.last_y), (ix, iy)):
                x = i[0]
                y = i[1]
                self.drawing[x, y, :] = iz, iz, iz
        self.last_x = ix
        self.last_y = iy


    def __from_homogeneous_to_real(self, point):
        return [point[0] / point[3], point[1] / point[3], point[2] / point[3]]

    def reset_graph(self):
        self.x = []
        self.y = []
        self.z = []
