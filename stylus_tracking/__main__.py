import tkinter as tk

from stylus_tracking.controller.controller import Controller
from stylus_tracking.ui.app import App

App(tk.Tk(), 'Stylus-tracking', Controller())
