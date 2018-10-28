import numpy as np
import cv2

video_capture = cv2.VideoCapture(0)


def next_frame():
    _, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    return gray
