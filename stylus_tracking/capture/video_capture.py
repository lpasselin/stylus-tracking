import numpy as np
import cv2
from cv2 import aruco


class VideoCapture:

    ARUCO_DICT = aruco.Dictionary_get(aruco.DICT_4X4_250)
    ARUCO_PARAMETERS = aruco.DetectorParameters_create()
    WIDTH = 600
    HEIGHT = 1200

    def __init__(self, video_source=0):
        self.video_capture = cv2.VideoCapture(video_source)
        if not self.video_capture.isOpened():
            raise ValueError("Unable to open video source {}.".format(video_source))
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)
        self.width = self.video_capture.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

    def get_next_frame(self):
        if self.video_capture.isOpened():
            ret, image = self.video_capture.read()
            if ret:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                return ret, image
            else:
                return ret, None

    def get_next_frame_with_aruco_label(self):
        ret, img_color = self.get_next_frame()
        img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
        img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)

        # Easily print aruco markers here: http://chev.me/arucogen/
        corners, ids, rejected_img_points = aruco.detectMarkers(img_gray,
                                                                self.ARUCO_DICT,
                                                                parameters=self.ARUCO_PARAMETERS)

        if np.any(ids):
            print(ids)
        if np.any(corners):
            print(corners)

        img_color_labeled = aruco.drawDetectedMarkers(img_color, corners)
        return img_color_labeled, corners, ids
