import math
import numpy as np


class Transform:

    def __init__(self):
        self.matrix = np.eye(4, dtype=np.float32)

    def set_translation(self, x, y, z):
        self.matrix[0:3, 3] = [x, y, z]

    def set_rotation(self, x, y, z):
        self.matrix[0:3, 0:3] = self.rodrigues(x, y, z)

    def translate(self, x=0, y=0, z=0, transform=None):
        if transform:
            new_transform = transform.copy()
        else:
            new_transform = Transform.from_parameters(x, y, z, 0, 0, 0)
        new_transform.combine(self)
        self.matrix = new_transform.matrix

        return self

    def inverse(self):
        ret = Transform()
        ret.matrix[0:3, 0:3] = self.matrix[0:3, 0:3].transpose()
        ret.matrix[0:3, 3] = -ret.matrix[0:3, 0:3].dot(self.matrix[0:3, 3])

        return ret

    def dot(self, points):
        shape = points.shape
        if shape[1] == 3:
            # to homogeneous (stack layer of one)
            ones = np.ones((shape[0], 1))
            homogeneous = np.hstack((points, ones)).T
        elif shape[1] == 4:
            homogeneous = points.T
        else:
            raise ValueError(
                "input array has to be of size 3 or in homogeneous coordinate, current size = " + str(shape))
        return self.matrix.dot(homogeneous).T[:, 0:3]

    def combine(self, transform, copy=False):
        ret_transform = self
        if not copy:
            self.matrix = self.matrix.dot(transform.matrix)
        else:
            new_matrix = self.matrix.dot(transform.matrix)
            ret_transform = Transform.from_matrix(new_matrix)

        return ret_transform

    def to_parameters(self, isDegree=False):
        x, y, z = self.matrix[0:3, 3]
        a, b, c = self.rodrigues_inverse(self.matrix[0:3, 0:3])
        if isDegree:
            a = math.degrees(a)
            b = math.degrees(b)
            c = math.degrees(c)
        ret = [x, y, z, a, b, c]

        return np.array(ret)

    @staticmethod
    def from_parameters(x, y, z, euler_x, euler_y, euler_z, is_degree=False):
        ret = Transform()
        ret.set_translation(x, y, z)
        if is_degree:
            euler_x = math.radians(euler_x)
            euler_y = math.radians(euler_y)
            euler_z = math.radians(euler_z)
        ret.set_rotation(euler_x, euler_y, euler_z)

        return ret

    @staticmethod
    def from_matrix(matrix):
        ret = Transform()
        ret.matrix = matrix

        return ret

    def __str__(self):
        params = self.to_parameters(isDegree=True)
        ret = ""
        ret += "x :" + str(params[0]) + ",\n"
        ret += "y :" + str(params[1]) + ",\n"
        ret += "z :" + str(params[2]) + ",\n"
        ret += "x :" + str(params[3]) + " degrees,\n"
        ret += "y :" + str(params[4]) + " degrees,\n"
        ret += "z :" + str(params[5]) + " degrees.\n"

        return ret

    def __repr__(self):
        return str(self.matrix)

    def rodrigues(self, x, y, z):
        matrix = np.eye(3)
        omega_skew = np.zeros((3, 3))
        omega_skew[0, 1] = -z
        omega_skew[1, 0] = z
        omega_skew[0, 2] = y
        omega_skew[2, 0] = -y
        omega_skew[1, 2] = -x
        omega_skew[2, 1] = x

        omega_skew_sqr = np.matmul(omega_skew, omega_skew)
        theta_sqr = x ** 2 + y ** 2 + z ** 2
        theta = math.sqrt(theta_sqr)
        sin_theta = math.sin(theta)

        if theta == 0:
            return np.eye(3)

        one_minus_cos_theta = 1 - math.cos(theta)
        one_minus_cos_div_theta_sqr = one_minus_cos_theta / theta_sqr

        sin_theta_div_theta_tensor = np.ones((3, 3))
        one_minus_cos_div_theta_sqr_tensor = np.ones((3, 3))

        if theta_sqr > 1e-12 and theta != 0:
            sin_theta_div_theta = sin_theta / theta
            sin_theta_div_theta_tensor.fill(sin_theta_div_theta)
            one_minus_cos_div_theta_sqr_tensor.fill(one_minus_cos_div_theta_sqr)
        else:
            sin_theta_div_theta_tensor.fill(1)
            one_minus_cos_div_theta_sqr_tensor.fill(0)
        matrix = matrix + np.multiply(sin_theta_div_theta_tensor, omega_skew) + \
                 np.multiply(one_minus_cos_div_theta_sqr_tensor, omega_skew_sqr)

        return matrix

    def rodrigues_inverse(self, matrix):
        x, y, z = 0, 0, 0
        r = matrix - matrix.T
        t = np.trace(matrix)
        if t >= 3. - 1e-12:
            w = (0.5 - ((t-3.)/12.)) * r
            x, y, z = w[2, 1], w[0, 2], w[1, 0]
        elif t > -1. + 1e-12:
            theta = math.acos((t - 1.) / 2.)
            w = (theta/(2.*math.sin(theta))) * r
            x, y, z = w[2, 1], w[0, 2], w[1, 0]
        else:
            diag = np.diag(matrix)
            a = np.argmax(diag)
            b = (a + 1) % 3
            c = (a + 2) % 3
            s = np.sqrt(diag[a] - diag[b] - diag[c] + 1)
            v = np.zeros(diag.shape)
            # unit quaternion (w, v)
            v[a] = s/2.
            v[b] = (1./(2.*s)) * (matrix[b, a] + matrix[a, b])
            v[c] = (1./(2.*s)) * (matrix[c, a] + matrix[a, c])
            v = math.pi * (v/np.linalg.norm(v))
            x, y, z = v[0], v[1], v[2]
        return x, y, z