import numpy as np
import cv2
from cv2 import aruco

video_capture = cv2.VideoCapture(0)

# TODO class
aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_250)
aruco_parameters = aruco.DetectorParameters_create()


def next_frame():
    _, img_color = video_capture.read()
    return img_color


def next_frame_with_aruco_label():
    img_color = next_frame()
    img_color = cv2.cvtColor(img_color, cv2.COLOR_BGR2RGB)
    img_gray = cv2.cvtColor(img_color, cv2.COLOR_RGB2GRAY)

    # Easily print aruco markers here: http://chev.me/arucogen/
    corners, ids, rejectedImgPoints = aruco.detectMarkers(img_gray, aruco_dict, parameters=aruco_parameters)

    if np.any(ids):
        print(ids)
    if np.any(corners):
        print(corners)

    img_color_labeled = aruco.drawDetectedMarkers(img_color, corners)
    return img_color_labeled, corners, ids
