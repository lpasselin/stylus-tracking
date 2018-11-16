import tkinter as tk

import cv2
from PIL import ImageTk, Image

from stylus_tracking.capture.video_capture import VideoCapture
from stylus_tracking.controller.controller import Controller


class App:
    DELAY = 10

    def __init__(self, window: tk.Tk, window_title: str, controller: Controller):
        self.window = window
        self.window.title(window_title)

        self.window.bind('<Escape>', lambda e: window.quit())
        self.window.config(background="#0F0F0F")

        self.controller = controller

        self.camera_canvas = tk.Canvas(window, width=VideoCapture.WIDTH, height=VideoCapture.HEIGHT)
        self.camera_canvas.pack(anchor=tk.W)

        # self.paper_canvas = tk.Canvas(window, width=self.controller.video_capture.WIDTH,
        #                               height=self.controller.video_capture.HEIGHT)
        # self.paper_canvas.pack(anchor=tk.E)

        self.calibrate_intrinsic_button = tk.Button(
            window, text="Calibrate intrinsic", command=self.controller.start_intrinsic_calibration)
        self.calibrate_intrinsic_button.pack()

        self.calibrate_intrinsic_button = tk.Button(
            window, text="Calculate extrinsic from intrinsic parameters", command=self.controller.calculate_extrinsic)
        self.calibrate_intrinsic_button.pack()

        self.current_image = None

        self.__update()

        self.window.mainloop()

    def __update(self):
        self.controller.next_frame()
        resized_image = cv2.resize(self.controller.model.current_frame, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        self.current_image = ImageTk.PhotoImage(image=Image.fromarray(resized_image))
        self.camera_canvas.create_image(0, 0, image=self.current_image, anchor=tk.NW)

        self.window.after(self.DELAY, self.__update)
