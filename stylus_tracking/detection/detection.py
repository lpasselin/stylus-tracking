import numpy as np
import cv2
from cv2 import aruco

from stylus_tracking.calibration import calibration

PENCIL_LENGTH = 153  # [mm] from dodecahedron center to tip of pencil.


class Detection:

    def __init__(self, cam_param: calibration):
        self.cam_param = cam_param
        self.success = False
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.parameters = aruco.DetectorParameters_create()
        #                   top left   top right  bot right   bot left
        points = dodecahedron_aruco_points()
        ids = np.array([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11]])
        self.board = aruco.Board_create(points, self.marker_dict, ids)
        self.pencil_tip_aruco_ref = pencil_tip_from_length_mm(PENCIL_LENGTH)

    def detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, self.marker_dict, parameters=self.parameters,
                                                              cameraMatrix=self.cam_param.intrinsic_parameters[
                                                                  'cameraMatrix'],
                                                              distCoeff=self.cam_param.intrinsic_parameters['distCoef'])

        self.success, rotation, translation = aruco.estimatePoseBoard(corners, ids, self.board,
                                                                      self.cam_param.intrinsic_parameters[
                                                                          'cameraMatrix'],
                                                                      self.cam_param.intrinsic_parameters[
                                                                          'distCoef'])

        if self.success:
            rvec = rotation.copy()
            tvec = translation.copy()

            img = aruco.drawDetectedMarkers(img, corners, ids)

            img = aruco.drawAxis(img, self.cam_param.intrinsic_parameters['cameraMatrix'],
                                   self.cam_param.intrinsic_parameters['distCoef'], rvec, tvec, length=100)

            print(rvec)
            print(tvec)

            pp = self.pencil_point

            # for now = > returns stylus position from the camera

            # TODO camera_to_stylus =
            # TODO world_to_stylus =

            # TODO return position + orientation of the stylus

            return img
        else:
            return img


# TODO new file
def rotation_around_y(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), 0, -np.sin(r), 0], [0, 1, 0, 0], [np.sin(r), 0, np.cos(r), 0], [0, 0, 0, 1]],
                     dtype=np.float32)


def rotation_around_z(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), np.sin(r), 0, 0], [-np.sin(r), np.cos(r), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                     dtype=np.float32)


def to_homogenous(a):
    size = a.shape[1]
    if size == 1:
        res = np.ones((size,1))
        res[:size, :] = a
    else:
        res = np.identity(size)
        res = np.identity(size)
        res[:size,:size] = a
    return res

def translation(tx, ty, tz):
    return np.matrix([[1, 0, 0, tx], [0, 1, 0, ty], [0, 0, 1, tz], [0, 0, 0, 1]], dtype=np.float32)


def hom2cart(p):
    return p[:-1] / p[-1]


def dodecahedron_aruco_points() -> np.array:
    radius = 25  # mm
    tc = 25 / 3  # mm translation in x and y of corners from center of face
    all_aruco_points = []
    origin_points = np.matrix([ [-tc, -tc, 0, 1],[-tc, tc, 0, 1],[tc, tc, 0, 1],[tc, -tc, 0, 1]], dtype=np.float32).T

    # first row
    for i in [2, 1, 0, 4, 3]:
        aruco_corners = rotation_around_z(72*i) * rotation_around_y(116.565) * \
                        rotation_around_z(180) * translation(0, 0, radius) * origin_points
        all_aruco_points.append(hom2cart(aruco_corners).T)
    # second row
    for i in [0, 4, 3, 2, 1]:
        aruco_corners = rotation_around_z(72 * i) * rotation_around_y(116.565) * translation(0, 0, -radius) * rotation_around_y(180) * origin_points
        all_aruco_points.append(hom2cart(aruco_corners).T)

    # top
    aruco_corners = translation(0, 0, radius) * origin_points
    all_aruco_points.append(hom2cart(aruco_corners).T)
    # bottom
    aruco_corners = translation(0, 0, -radius) * rotation_around_y(180) * origin_points
    all_aruco_points.append(hom2cart(aruco_corners).T)

    all_aruco_points = np.array(all_aruco_points, dtype=np.float32)
    return all_aruco_points

def pencil_tip_from_length_mm(pencil_length):
    zero_point = np.array([[0], [0], [0], [1]])
    pencil_tip = rotation_around_y(116.565 / 3) * translation(0, 0, -pencil_length) * zero_point
    return pencil_tip
