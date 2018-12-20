import sys
from logging import Logger

from stylus_tracking.calibration import calibration
from stylus_tracking.calibration.calibration import State
from stylus_tracking.capture.video_capture import VideoCapture
from stylus_tracking.controller.model import AppModel
from stylus_tracking.detection import detection


class Controller:

    BUFFER_SIZE = 3

    def __init__(self, logger: Logger, video_source=0):
        self.logger = logger
        self.video_capture = VideoCapture(video_source)
        self.calibration = calibration.Calibration(self.logger.getChild("Calibration"))
        self.state = State.RAW
        self.detection = None

        self.model = AppModel()
        self.buffer = []

    def next_frame(self):
        ret, frame = self.video_capture.get_next_frame()
        self.model.current_frame = frame
        refresh = False
        if ret:
            self.model.current_frame = frame
            if self.state is State.CALIBRATING_INTRINSIC:
                if self.calibration.calculate_intrinsic(frame):
                    self.state = State.CALIBRATED_INTRINSIC
            if self.state is State.CALIBRATING_EXTRINSIC:
                if self.calibration.calculate_extrinsic(self.model.current_frame):
                    self.state = State.CALIBRATED
                    self.detection = detection.Detection(self.calibration)
                else:
                    self.state = State.CALIBRATED_INTRINSIC
            if self.state is State.CALIBRATED:
                if self.detection is not None:
                    self.model.current_frame, point = self.detection.detect(frame)
                    if point is not None:
                        self.buffer.append(point)
                        if len(self.buffer) == self.BUFFER_SIZE:
                            self.buffer = sorted(self.buffer)
                            self.model.add_point(self.buffer[(self.BUFFER_SIZE-1)//2])
                            self.buffer = []
                            refresh = True
                    else:
                        sys.stdout.write('\a')
                        sys.stdout.flush()
                else:
                    self.logger.info("Calibration should be performed prior to detection.")
        return refresh

    def start_intrinsic_calibration(self) -> None:
        self.state = State.CALIBRATING_INTRINSIC
        self.calibration.start_intrinsic_calibration()

    def calculate_extrinsic(self) -> None:
        if self.state is not State.CALIBRATED_INTRINSIC:
            self.logger.info("Intrinsic calibration should be performed prior to the extrinsic one.")
        else:
            self.state = State.CALIBRATING_EXTRINSIC

    def try_load_previous_intrinsic_calibration_parameters(self) -> None:
        if self.calibration.try_load_intrinsic():
            self.state = State.CALIBRATED_INTRINSIC

    def reset_extrinsic_calibration(self) -> None:
        self.state = State.CALIBRATING_EXTRINSIC
