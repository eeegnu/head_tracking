
import cv2 as cv
import numpy as np
import math
import time
from icecream import ic
# from constants import *
from constants import WHITE, RED, GREEN, ROOM_WIDTH, ROOM_HEIGHT, scalez
from geometry import projection, darken


class Target:
    def __init__(self, z, x, y, radius, color=RED):
        """
        @param xyz
            (x, y, z)
        """
        self.x, self.y, self.z = x, y, z
        self.radius = radius
        self.color = color
    
    def draw(self, img, camera):
        if camera[2] <= self.z:
            return
        px, py, pz = projection((self.x, self.y, self.z), camera)
        edge = projection((self.x+self.radius, self.y, self.z), camera)
        radius = edge[0] - px
        shade = math.exp(-abs((camera[2] - self.z)/200))
        cv.circle(img, (px, py), radius, darken(self.color, shade), -1)
        cv.circle(img, (px, py), radius*2//3, darken(WHITE, shade), radius//6)
        cv.circle(img, (px, py), radius*1//3, darken(WHITE, shade), radius//6)


class Frame:
    def __init__(self, z, x=0, y=0, base_color=WHITE):
        # assert z <= 0
        self.x, self.y, self.z = x, y, z
        self.w = ROOM_WIDTH - 2 * self.x
        self.h = ROOM_HEIGHT - 2 * self.y
        self.base_color = base_color

    def draw(self, img, camera):
        cx, cy, cz = camera
        if camera[2] <= self.z:
            return
        proj1 = projection((self.x, self.y, self.z), camera)
        proj2 = projection((self.x+self.w, self.y+self.h, self.z), camera)
        if proj1 is None or proj2 is None:
            return
        self.x1, self.y1, _ = proj1
        self.x2, self.y2, _ = proj2

        shade = math.exp(-abs((self.z - cz)/(4*scalez)))
        self.color = darken(self.base_color, shade)

        cv.rectangle(img, (self.x1, self.y1), (self.x2, self.y2), self.color, 1)


class Room:
    def __init__(self, dz=25, n=50):
        self.frames = [Frame(z=-i*dz) for i in range(0, n)]
        self.all = self.frames
        self.all.append(Target(z=-12*dz, x=ROOM_WIDTH*2//3, y=ROOM_HEIGHT*2//3, radius=200, color=GREEN))
        self.all.append(Target(z=-8*dz, x=ROOM_WIDTH//2, y=ROOM_HEIGHT//2, radius=100))
        self.all.append(Target(z=-2*dz, x=ROOM_WIDTH//4, y=ROOM_HEIGHT//4, radius=100))


    def draw(self, img, camera):
        frames = self.frames

        for each in self.all:
            each.draw(img, camera)

        # ic(self.all[1].x1, self.all[1].y1, self.all[1].x2, self.all[1].y2)
        
        # for f, s in zip(frames[:-1], frames[1:]):
        #     cv.line(img, (0, 0), (frames[-1].x1, frames[-1].y1), (255,0,0), 2)
