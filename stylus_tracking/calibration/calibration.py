import numpy as np
from stylus_tracking.capture import capture
import cv2
import time


class Calibration():
    INTRINSIC_PARAMETERS_FILENAME = "/myapp/stylus_tracking/intrinsic_parameters.npz"

    CORNERS_IDS = (100, 101, 102, 103)

    # Center as origin (0, 0, 0)
    OBJECT_POINTS = np.zeros((4, 3))
    OBJECT_POINTS[0] = [-101.45, -133.2, 0]
    OBJECT_POINTS[1] = [101.45, -133.2, 0]
    OBJECT_POINTS[2] = [101.45, 133.2, 0]
    OBJECT_POINTS[3] = [-101.45, 133.2, 0]

    def __init__(self):
        self.rvecs = None
        self.tvecs = None
        self.intrinsic_parameters = None
        self.try_load_intrinsic()

    def calculate_extrinsic(self, corners, ids):
        if np.any(ids) and np.all(np.in1d(self.CORNERS_IDS, ids)):
            image_points = np.zeros((4, 2))
            for id, corner in zip(ids, corners):
                index = self.CORNERS_IDS.index(id)
                image_points[index] = corner[0, index, :]

            _, self.rvecs, self.tvecs = cv2.solvePnP(self.OBJECT_POINTS, image_points,
                                                     self.intrinsic_parameters['cameraMatrix'],
                                                     self.intrinsic_parameters['distCoef'])
            return True
        return False

    def try_load_intrinsic(self) -> bool:
        try:
            self.intrinsic_parameters = np.load(self.INTRINSIC_PARAMETERS_FILENAME)['intrinsic_parameters']
        except IOError:
            return False
        return True

    def calculate_intrinsic(self) -> None:
        # Idea: use drawing area aruco corners for intrinsic calibration?
        # termination criteria
        # TODO find optimal criteria for our use case
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        # prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
        objp = np.zeros((10 * 7, 3), np.float32)
        objp[:, :2] = np.mgrid[0:10, 0:7].T.reshape(-1, 2)

        objpoints = []  # 3d point in real world space
        imgpoints = []  # 2d points in image plane.
        valid_frames = 0
        while valid_frames < 10:
            time.sleep(0.5)
            print("Show checkerboard for intrinsic calibration: %s/10" % valid_frames)
            frame = capture.next_frame()
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            ret, corners = cv2.findChessboardCorners(frame, (10, 7), None)  # Checkerboard 11x8 (23mmx23mm) each
            if ret:
                valid_frames += 1
                corners2 = cv2.cornerSubPix(frame, corners, (11, 11), (-1, -1), criteria)
                objpoints.append(objp)
                imgpoints.append(corners2)

        ret, cameraMatrix, distCoef, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, frame.shape[::-1], None,
                                                                        None)
        self.intrinsic_parameters = {
            'cameraMatrix': cameraMatrix,
            'distCoef': distCoef,
            # 'rvecs': self.rvecs, 'tvecs': self.tvecs,
        }
        self.save_intrinsic()

    def save_intrinsic(self):
        np.savez(self.INTRINSIC_PARAMETERS_FILENAME, intrinsic_parameters=self.intrinsic_parameters)
