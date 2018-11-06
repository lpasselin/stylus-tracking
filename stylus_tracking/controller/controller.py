from enum import Enum, auto
from stylus_tracking.capture import capture
from stylus_tracking.calibration import calibration


class State(Enum):
    CALIBRATING_INTRINSIC = auto()
    CALIBRATING_EXTRINSIC = auto()
    CALIBRATED = auto()


class Controller:

    def __init__(self):
        self.calibration = calibration.Calibration()
        self.state = State.CALIBRATING_INTRINSIC

    def next_frame(self):
        frame, corners, ids = capture.next_frame_with_aruco_label()

        if self.state == State.CALIBRATED:
            pass

        elif self.state == State.CALIBRATING_INTRINSIC:
            if self.calibration.try_load_intrinsic() == False:
                self.calibration.calculate_intrinsic()
            self.state = State.CALIBRATING_EXTRINSIC

        elif self.state == State.CALIBRATING_EXTRINSIC:
            if self.calibration.calculate_extrinsic(corners, ids):
                self.state = State.CALIBRATED

        return frame
