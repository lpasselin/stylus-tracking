import tkinter as tk

import cv2
import numpy as np
from PIL import ImageTk, Image

from stylus_tracking.capture.video_capture import VideoCapture
from stylus_tracking.controller.controller import Controller
from stylus_tracking.ui.graph import Graph


class App:
    DELAY = 10
    RESIZE_FACTOR = 1
    COLOR = "#e6e6e6"

    def __init__(self, window: tk.Tk, window_title: str, controller: Controller, logger):
        self.window = window

        self.window.title(window_title)

        self.window.bind('<Escape>', lambda e: window.quit())
        self.window.config(background=self.COLOR)

        self.controller = controller

        self.current_graph = Graph(self.window, 10, 8)

        self.logger = logger

        self.camera_frame = None
        self.calibration_buttons = None
        self.calibrate_intrinsic_button = None
        self.load_previous_intrinsic_parameters_button = None
        self.calibrate_extrinsic_button = None
        self.reset_extrinsic_calibration_button = None

        self.reset_graph = tk.Button(self.window,
                                     text="Reset graph",
                                     command=self.__reset_graph)
        self.reset_graph.grid(row=2, column=1)

        self.calibration_button = tk.Button(self.window,
                                            text="Calibration window",
                                            command=self.__calibration_child)
        self.calibration_button.grid(row=3, column=1)

        self.current_image = None

        self.__update()

        self.window.mainloop()

    def __update(self):
        self.controller.next_frame()
        if self.camera_frame is not None:
            resized_image = cv2.resize(self.controller.model.current_frame, None,
                                       fx=self.RESIZE_FACTOR, fy=self.RESIZE_FACTOR, interpolation=cv2.INTER_LINEAR)
            self.current_image = ImageTk.PhotoImage(image=Image.fromarray(np.fliplr(resized_image)))
            self.camera_canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)
        self.__update_graphic()

        self.window.after(self.DELAY, self.__update)

    def __update_graphic(self):
        self.current_graph.update(self.controller.model.x, self.controller.model.y, self.controller.model.z)

    def __reset_graph(self):
        self.controller.model.reset_graph()

    def __calibration_child(self):
        self.camera_frame = tk.Toplevel(self.window)
        self.camera_canvas = tk.Canvas(self.camera_frame,
                                       width=VideoCapture.WIDTH * self.RESIZE_FACTOR,
                                       height=VideoCapture.HEIGHT * self.RESIZE_FACTOR,
                                       background=self.COLOR)

        self.camera_canvas.grid(row=2, column=1)
        self.calibration_buttons = tk.Canvas(self.camera_frame,
                                             width=self.window.winfo_width(),
                                             background=self.COLOR)
        self.calibration_buttons.grid(row=3, column=1, columnspan=2)
        self.calibrate_intrinsic_button = tk.Button(self.calibration_buttons,
                                                    text="Calibrate intrinsic",
                                                    command=self.controller.start_intrinsic_calibration)
        self.calibrate_intrinsic_button.grid(row=1, column=1)
        self.load_previous_intrinsic_parameters_button = tk.Button(self.calibration_buttons,
                                                                   text="Load previous intrinsic parameters",
                                                                   command=self.controller.try_load_previous_intrinsic_calibration_parameters)
        self.load_previous_intrinsic_parameters_button.grid(row=2, column=1)
        self.calibrate_extrinsic_button = tk.Button(self.calibration_buttons,
                                                    text="Calculate extrinsic from intrinsic parameters",
                                                    command=self.controller.calculate_extrinsic)
        self.calibrate_extrinsic_button.grid(row=3, column=1)
        self.reset_extrinsic_calibration_button = tk.Button(self.calibration_buttons,
                                                            text="Reset extrinsic calibration",
                                                            command=self.controller.reset_extrinsic_calibration)
        self.reset_extrinsic_calibration_button.grid(row=4, column=1)

        self.done_button = tk.Button(self.calibration_buttons,
                                     text="Done",
                                     command=self.__close_camera_frame)
        self.done_button.grid(row=5, column=1)

    def __close_camera_frame(self):
        self.camera_frame.destroy()
        self.camera_frame = None
