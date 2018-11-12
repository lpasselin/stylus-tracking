from enum import Enum, auto

from stylus_tracking.calibration import calibration
from stylus_tracking.capture.video_capture import VideoCapture


class State(Enum):
    CALIBRATING_INTRINSIC = auto()
    CALIBRATING_EXTRINSIC = auto()
    CALIBRATED = auto()


class Controller:

    def __init__(self, video_source=0):
        self.video_capture = VideoCapture(video_source)
        self.calibration = calibration.Calibration()
        self.state = State.CALIBRATING_INTRINSIC

    def next_frame(self):
        frame, corners, ids = self.video_capture.get_next_frame_with_aruco_label()

        self.__update_state(corners, ids)

        return frame

    def __update_state(self, corners, ids):
        if self.state == State.CALIBRATED:
            pass
                if self.state == State.CALIBRATED:
            pass

        elif self.state == State.CALIBRATING_INTRINSIC:
            if self.calibration.try_load_intrinsic() == False:
                self.calibration.calculate_intrinsic()
                
            self.state = State.CALIBRATING_EXTRINSIC

        elif self.state == State.CALIBRATING_EXTRINSIC:
            if self.calibration.calculate_extrinsic(corners, ids):
                self.state = State.CALIBRATED
