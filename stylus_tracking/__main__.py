import logging
import os
import time
import tkinter as tk

from stylus_tracking.controller.controller import Controller
from stylus_tracking.ui.app import App

logger = logging.getLogger()
log_formatter = logging.Formatter("%(asctime)s [%(threadName)-7.7s][%(levelname)-5.5s] %(message)s")

console_handler = logging.StreamHandler()
console_handler.setFormatter(log_formatter)
logger.addHandler(console_handler)

logger.setLevel(logging.INFO)

log_directory = os.path.join(os.path.dirname(__file__), "logs")

try:
    if not os.path.exists(log_directory):
        os.makedirs(log_directory)

    log_file: str = log_directory.format(date=time.strftime("%Y-%m-%d-%Hh%Mm%Ss"))

    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(log_formatter)
    logger.addHandler(file_handler)

except IsADirectoryError:
    logger.info("Could not create log directory")

App(tk.Tk(), 'Stylus-tracking', Controller(logger.getChild("Controller")), logger.getChild("App"))
