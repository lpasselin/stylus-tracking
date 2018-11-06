from enum import Enum, auto
from stylus_tracking.capture import capture
from stylus_tracking.calibration import calibration

class State(Enum):
    CALIBRATING = auto()
    CALIBRATED = auto()

class Controller():

    def __init__(self):
        self.calibration = calibration.Calibration()
        self.state = State.CALIBRATING

    def next_frame(self):
        frame, corners, ids  = capture.next_frame_with_aruco_label()

        if self.state == State.CALIBRATING:
            if self.calibration.calculate_extrinsic(corners, ids):
                self.state = State.CALIBRATED

        if self.state == State.CALIBRATED:
            pass

        return frame
