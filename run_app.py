import threading
import subprocess
import sys
import os
import time

def resource_path(relative_path):
    if hasattr(sys, "_MEIPASS"):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def start_controller():
    controller = resource_path("gesture_engine/controller.py")
    subprocess.call([sys.executable, controller])

t = threading.Thread(target=start_controller)
t.start()
