import time
from enum import Enum, auto
from logging import Logger

import cv2
import numpy as np
from cv2 import aruco


class State(Enum):
    RAW = auto()
    CALIBRATING_INTRINSIC = auto()
    CALIBRATED_INTRINSIC = auto()
    CALIBRATING_EXTRINSIC = auto()
    CALIBRATED = auto()


class Calibration:
    INTRINSIC_PARAMETERS_FILENAME = "/myapp/stylus_tracking/intrinsic_parameters.npz"
    ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_4X4_250)
    ARUCO_PARAMETERS = aruco.DetectorParameters_create()

    CORNERS_IDS = (100, 101, 102, 103)

    # Center as origin (0, 0, 0)
    OBJECT_POINTS = np.zeros((4, 3))
    OBJECT_POINTS[0] = [-101.45, -133.2, 0]
    OBJECT_POINTS[1] = [101.45, -133.2, 0]
    OBJECT_POINTS[2] = [101.45, 133.2, 0]
    OBJECT_POINTS[3] = [-101.45, 133.2, 0]

    def __init__(self, logger: Logger):
        self.rvecs = None
        self.tvecs = None
        self.intrinsic_parameters = None
        self.try_load_intrinsic()
        self.state = State.RAW
        self.logger = logger

        self.criteria = None
        self.objp = None
        self.objpoints = None
        self.imgpoints = None
        self.valid_frames = None
        self.frame_counter = None

    def try_load_intrinsic(self) -> bool:
        try:
            self.intrinsic_parameters = np.load(self.INTRINSIC_PARAMETERS_FILENAME)['intrinsic_parameters']
        except IOError:
            return False
        return True

    def calculate_extrinsic(self, frame) -> bool:
        self.logger.info("Starting EXTRINSIC calibration.")
        _, corners, ids = self.get_frame_with_aruco_label(frame)
        if np.any(ids) and np.all(np.in1d(self.CORNERS_IDS, ids)):
            image_points = np.zeros((4, 2))
            for id, corner in zip(ids, corners):
                index = self.CORNERS_IDS.index(id)
                image_points[index] = corner[0, index, :]

            _, self.rvecs, self.tvecs = cv2.solvePnP(self.OBJECT_POINTS, image_points,
                                                     self.intrinsic_parameters['cameraMatrix'],
                                                     self.intrinsic_parameters['distCoef'])
            self.logger.info("Extrinsic calibration calculated.")
            return True
        self.logger.error("Extrinsic calibration could not be completed.")
        return False

    def calculate_intrinsic(self, frame) -> None:
        if self.frame_counter < 30:
            self.frame_counter += 1
            return 

        elif self.valid_frames < 10:
            self.frame_counter = 0
            self.logger.info("Show checkerboard for intrinsic calibration: %s/10." % self.valid_frames)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
            ret, corners = cv2.findChessboardCorners(frame, (10, 7), None)  # Checkerboard 11x8 (23mmx23mm) each
            if ret:
                self.valid_frames += 1
                corners2 = cv2.cornerSubPix(frame, corners, (11, 11), (-1, -1), self.criteria)
                self.objpoints.append(self.objp)
                self.imgpoints.append(corners2)

        if self.valid_frames >= 10:
            ret, cameraMatrix, distCoef, rvecs, tvecs = cv2.calibrateCamera(self.objpoints, self.imgpoints, frame.shape[::-1], None, None)
            self.intrinsic_parameters = {
                'cameraMatrix': cameraMatrix,
                'distCoef': distCoef,
                # 'rvecs': self.rvecs, 'tvecs': self.tvecs,
            }
            self.save_intrinsic()
            self.logger.info("Intrinsic calibration saved.")

    def start_intrinsic_calibration(self) -> None:
        # Idea: use drawing area aruco corners for intrinsic calibration?
        # termination criteria
        # TODO find optimal criteria for our use case
        self.criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        self.objp = np.zeros((10 * 7, 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2)
        self.objpoints = []  # 3d point in real world space
        self.imgpoints = []  # 2d points in image plane.
        self.valid_frames = 0
        self.frame_counter = 0
        self.logger.info("Starting INTRINSIC calibration.")

    def save_intrinsic(self) -> None:
        np.savez(self.INTRINSIC_PARAMETERS_FILENAME, intrinsic_parameters=self.intrinsic_parameters)

    def get_frame_with_aruco_label(self, image):
        image_grey = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

        # Easily print aruco markers here: http://chev.me/arucogen/
        corners, ids, rejected_img_points = aruco.detectMarkers(image_grey,
                                                                self.ARUCO_DICT, parameters=self.ARUCO_PARAMETERS)

        if np.any(ids):
            print(ids)
        if np.any(corners):
            print(corners)

        img_color_labeled = aruco.drawDetectedMarkers(image, corners)
        return img_color_labeled, corners, ids
