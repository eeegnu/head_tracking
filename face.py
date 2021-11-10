
import cv2 as cv
import numpy as np
from icecream import ic
from constants import RED, GREEN, CAM_WIDTH, CAM_HEIGHT


class Part:
    def __init__(self, cascade_file, color, draw_func, decay=0.5, img=None, region=(None, None, None, None)):
        """
        @param cascade_file: str
            ex 'data/cascade_eye.xml'
        @param img
            colored image
        @param region
            (x, y, w, h)
        """
        self.cascade = cv.CascadeClassifier(cascade_file)
        self.img = img
        self.color = color
        self.draw_func = draw_func
        self.x, self.y, self.w, self.h = region
        self.decay = decay
    
    def detect(self, img):
        self.img = img
        self.gray = cv.cvtColor(self.img, cv.COLOR_BGR2GRAY)
        rects = self.cascade.detectMultiScale(self.gray, scaleFactor=1.3, minNeighbors=5, minSize=(20,20))
        rect = self._largest(rects)
        if rect is not None:
            self._update_region(rect)
        return rect

    def draw(self, img):
        if (img is not None) and (self.x is not None):
            self.draw_func(img, (self.x, self.y), (self.x+self.w, self.y+self.h), self.color, 2)

    def _largest(self, rects):
        if len(rects) == 0:
            return None
        return sorted(rects, key=lambda x: x[2])[0]
    
    def _update_region(self, rect):
        if self.x is None:
            self.x, self.y, self.w, self.h = rect
        else:
            x, y, w, h = rect
            self.x = int(self.decay * self.x + (1 - self.decay) * x)
            self.y = int(self.decay * self.y + (1 - self.decay) * y)
            self.w = int(self.decay * self.w + (1 - self.decay) * w)
            self.h = int(self.decay * self.h + (1 - self.decay) * h)

    @property
    def region(self):
        return (self.x, self.y, self.w, self.h)


class Face(Part):
    def __init__(self, **kwargs):
        super().__init__(cascade_file='data/cascade_face.xml', color=GREEN, draw_func=cv.rectangle, **kwargs)
    
    def detect(self, img):
        super().detect(img)

    def draw(self, img):
        super().draw(img)

    @property
    def cx(self):
        return self.x + self.w / 2

    @property
    def cy(self):
        return self.y + self.h / 2

    def coordinates(self):
        """returns (cx, cy, cz) in [0, 1]x[0,1]x[0,inf)"""
        if self.x is None:
            return [0.5, 0.5, 1]

        maxw = min(CAM_WIDTH, CAM_HEIGHT)
        return [self.cx / CAM_WIDTH, self.cy / CAM_HEIGHT, maxw/ self.w]  # TODO
    
