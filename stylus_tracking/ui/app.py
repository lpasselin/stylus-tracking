import tkinter as tk

import cv2
import numpy as np
from PIL import ImageTk, Image

from stylus_tracking.capture.video_capture import VideoCapture
from stylus_tracking.controller.controller import Controller
from stylus_tracking.ui.graph import Graph


class App:
    DELAY = 1
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
        self.camera_canvas = None

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
        refresh = self.controller.next_frame()
        if self.camera_frame is not None:
            resized_image = cv2.resize(self.controller.model.current_frame, None,
                                       fx=self.RESIZE_FACTOR, fy=self.RESIZE_FACTOR, interpolation=cv2.INTER_LINEAR)
            self.current_image = ImageTk.PhotoImage(image=Image.fromarray(np.fliplr(resized_image)))
            self.camera_canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)
        if refresh:
            self.__update_graphic()
        self.window.after(self.DELAY, self.__update)

    def __update_graphic(self):
        if self.controller.model.new_x is not None:
            self.current_graph.update(self.controller.model.new_x, self.controller.model.new_y, self.controller.model.new_z)

    def __reset_graph(self):
        self.current_graph.reset()

    def __calibration_child(self):
        self.camera_frame = tk.Toplevel(self.window)
        self.camera_frame.bind('<Escape>', self.__close_camera_frame)
        self.camera_frame.protocol('WM_DELETE_WINDOW', self.__close_camera_frame)
        self.camera_canvas = tk.Canvas(self.camera_frame,
                                       width=VideoCapture.WIDTH * self.RESIZE_FACTOR,
                                       height=VideoCapture.HEIGHT * self.RESIZE_FACTOR,
                                       background=self.COLOR)

        self.camera_canvas.grid(row=2, column=1)
        calibration_buttons = tk.Canvas(self.camera_frame,
                                        width=self.window.winfo_width(),
                                        background=self.COLOR)
        calibration_buttons.grid(row=3, column=1, columnspan=2)
        calibrate_intrinsic_button = tk.Button(calibration_buttons,
                                               text="Calibrate intrinsic",
                                               command=self.controller.start_intrinsic_calibration)
        calibrate_intrinsic_button.grid(row=1, column=1)
        load_previous_intrinsic_parameters_button = tk.Button(calibration_buttons,
                                                              text="Load previous intrinsic parameters",
                                                              command=self.controller.try_load_previous_intrinsic_calibration_parameters)
        load_previous_intrinsic_parameters_button.grid(row=2, column=1)
        calibrate_extrinsic_button = tk.Button(calibration_buttons,
                                               text="Calculate extrinsic from intrinsic parameters",
                                               command=self.controller.calculate_extrinsic)
        calibrate_extrinsic_button.grid(row=3, column=1)
        reset_extrinsic_calibration_button = tk.Button(calibration_buttons,
                                                       text="Reset extrinsic calibration",
                                                       command=self.controller.reset_extrinsic_calibration)
        reset_extrinsic_calibration_button.grid(row=4, column=1)

        done_button = tk.Button(calibration_buttons,
                                text="Done",
                                command=self.__close_camera_frame)
        done_button.grid(row=5, column=1)

    def __close_camera_frame(self):
        self.camera_frame.destroy()
        self.camera_frame = None
