import cv2


class VideoCapture:
    HEIGHT = 1200
    WIDTH = 1600

    def __init__(self, video_source=0):
        self.video_capture = cv2.VideoCapture(video_source)
        if not self.video_capture.isOpened():
            raise ValueError("Unable to open video source {}.".format(video_source))
        self.video_capture.set(cv2.CAP_PROP_FRAME_WIDTH, self.WIDTH)
        self.video_capture.set(cv2.CAP_PROP_FRAME_HEIGHT, self.HEIGHT)

    def __del__(self):
        if self.video_capture.isOpened():
            self.video_capture.release()

    def get_next_frame(self) -> (bool, any):
        if self.video_capture.isOpened():
            ret, image = self.video_capture.read()
            if ret:
                image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
                return ret, image
            else:
                return ret, None
