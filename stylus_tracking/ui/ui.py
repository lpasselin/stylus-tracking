import tkinter as tk
import numpy as np
from PIL import Image, ImageTk
from stylus_tracking.capture import capture

window = tk.Tk()
window.bind('<Escape>', lambda e: window.quit())
window.config(background="#0F0F0F")
mainFrame = tk.Frame(window, width=720, height=720)
mainFrame.grid(row=0, column=0, padx=10, pady=2)
mainFrame.columnconfigure(0, weight=1)
mainFrame.columnconfigure(1, weight=1)
labelImage1 = tk.Label(mainFrame, text="Image1")
labelImage2 = tk.Label(mainFrame, text="Image2")
labelImage1.grid(row=0, column=0, sticky=tk.W)
labelImage2.grid(row=0, column=1, sticky=tk.E)


def show_frame():
    frame = capture.next_frame()
    img = Image.fromarray(frame)
    imgtk = ImageTk.PhotoImage(image=img)
    labelImage1.image = imgtk
    labelImage1.configure(image=imgtk)
    labelImage1.after(10, show_frame)


def show_frame2():
    cv2image = np.array([list(range(255)) for _ in range(100)], dtype=np.uint8)
    img = Image.fromarray(cv2image)
    imgtk = ImageTk.PhotoImage(image=img)
    labelImage2.image = imgtk
    labelImage2.configure(image=imgtk)
    labelImage2.after(10, show_frame2)


def main():
    show_frame()
    # show_frame2()
    window.mainloop()


if __name__ == '__main__':
    main()