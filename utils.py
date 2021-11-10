
import sys
import cv2 as cv

from constants import CAM_WIDTH, CAM_HEIGHT
from constants import font, fontScale, fontColor, lineType


def setup_capture():
    """Initializes video capture (camera) device"""
    cap = cv.VideoCapture(0)
    cap.set(cv.CAP_PROP_FRAME_WIDTH, CAM_WIDTH)
    cap.set(cv.CAP_PROP_FRAME_HEIGHT, CAM_HEIGHT)
    if cap.isOpened():
        return cap
    print("Cannot open camera")
    sys.exit()


class Timer:
    """Used to track fps and frame number"""
    def __init__(self, decay=0.9):
        self.decay = decay

        self.last_time = cv.getTickCount()
        self.fps = 30
        self.frame = 0
    
    def tick(self):
        """Returns new fps"""
        self.frame += 1
        current_time = cv.getTickCount()
        current_fps = cv.getTickFrequency() / (current_time - self.last_time)
        self.last_time = current_time

        self.fps = self.decay * self.fps + (1 - self.decay) * current_fps
        return self.fps


def add_text(img, text, position):
    """position - bottomLeftCornerOfText"""
    cv.putText(
        img, 
        text, 
        position,
        font, 
        fontScale,
        fontColor,
        lineType
    )