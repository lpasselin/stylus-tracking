import tkinter as tk

from PIL import ImageTk, Image

from stylus_tracking.controller.controller import Controller


class App:
    DELAY = 10

    def __init__(self, window: tk.Tk, window_title: str, controller: Controller):
        self.window = window
        self.window.title(window_title)

        self.window.bind('<Escape>', lambda e: window.quit())
        self.window.config(background="#0F0F0F")

        self.controller = controller

        self.canvas = tk.Canvas(window, width=self.controller.video_capture.width,
                                height=self.controller.video_capture.height)
        self.canvas.pack()

        self.camera_image = None

        self.update()

        self.window.mainloop()

    def update(self):
        ret, img = self.controller.video_capture.get_next_frame()
        self.controller.next_frame()

        if ret:
            self.camera_image = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.canvas.create_image(0, 0, image=self.camera_image, anchor=tk.NW)

        self.window.after(self.DELAY, self.update)
