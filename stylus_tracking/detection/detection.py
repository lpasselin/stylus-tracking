import numpy as np
import cv2
from cv2 import aruco

from stylus_tracking.calibration import calibration


class Detection:

    def __init__(self, cam_param: calibration):
        self.cam_param = cam_param
        self.success = False
        self.marker_dict = aruco.Dictionary_get(aruco.DICT_ARUCO_ORIGINAL)
        self.parameters = aruco.DetectorParameters_create()
        points = []  # TODO all 4 corners for each marker
        ids = np.array([[0], [1], [2], [3], [4], [5], [6], [7], [8], [9], [10], [11]])
        self.board = aruco.Board_create(points, self.marker_dict, ids)

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

            print(rvec)
            print(tvec)

            # for now = > returns stylus position from the camera

            # TODO camera_to_stylus =
            # TODO world_to_stylus =

            # TODO return position + orientation of the stylus

            return None
        else:
            return None
