import numpy as np

class Calibration():
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

    def calculate_extrinsic(self, corners, ids):
        if np.any(ids) and np.all(np.in1d(self.CORNERS_IDS, ids)):
            image_points = np.zeros((4, 2))
            for id, corner in zip(ids, corners):
                index = self.CORNERS_IDS.index(id)
                image_points[index] = corner[0, index, :]

            # TODO : Need intrinsic matrix and distortion
            # _, self.rvecs, self.tvecs = cv2.solvePnP(self.OBJECT_POINTS, image_points,
            #                                         self.INTRINSIC_MATRIX, self.DISTORTION)
            return True
        return False

