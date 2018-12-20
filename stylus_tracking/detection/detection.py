import math
import numpy as np
import cv2
from cv2 import aruco

from stylus_tracking.calibration import calibration
from stylus_tracking.detection import transform

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

            #print(rvec)
            #print(tvec)

            camera_to_stylus = transform.Transform.from_parameters(np.asscalar(tvec[0]), np.asscalar(tvec[1]),
                                                         np.asscalar(tvec[2]), np.asscalar(rvec[0]),
                                                         np.asscalar(rvec[1]), np.asscalar(rvec[2]))

            # TODO return position + orientation of the stylus

            camera_to_world = transform.Transform.from_parameters(np.asscalar(self.cam_param.tvecs[0]),
                                                        np.asscalar(self.cam_param.tvecs[1]),
                                                        np.asscalar(self.cam_param.tvecs[2]),
                                                        np.asscalar(self.cam_param.rvecs[0]),
                                                        np.asscalar(self.cam_param.rvecs[1]),
                                                        np.asscalar(self.cam_param.rvecs[2]))

            world_to_camera = camera_to_world.inverse()

            world_to_stylus = world_to_camera.combine(camera_to_stylus, True)

            translation_stylus = rotation_around_y(116.565 / 3) * translation(0, 0, -PENCIL_LENGTH)

            world_to_stylus.translate(translation_stylus[0], translation_stylus[1], translation_stylus[2])

            stylus_info = world_to_stylus.to_parameters(True)
            position_x = stylus_info[0]
            position_y = stylus_info[1]
            position_z = stylus_info[2]

            print(position_x, position_y, position_z)

            return img, (position_x, position_y, position_z, 1)
        else:
            return img, None


# TODO new file
def rotation_around_y(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), 0, -np.sin(r), 0], [0, 1, 0, 0], [np.sin(r), 0, np.cos(r), 0], [0, 0, 0, 1]],
                     dtype=np.float32)


def rotation_around_z(d):
    r = np.deg2rad(d)
    return np.matrix([[np.cos(r), np.sin(r), 0, 0], [-np.sin(r), np.cos(r), 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]],
                     dtype=np.float32)


def to_homogenous_position(a):
    size = a.shape[0]
    res = np.ones((size+1, 1))
    res[:size, :] = a
    return res

def to_homogenous_translation(a):
    size = a.shape[0]
    res = np.identity(size+1)
    res[:size,size] = a.flatten()
    return res

def to_homogenous_rotation(a):
    size = a.shape[0]
    res = np.identity(size+1)
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
