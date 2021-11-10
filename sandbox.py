
import cv2 as cv
import numpy as np
from icecream import ic

import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from face import Face
from utils import Timer, setup_capture, add_text


cap = setup_capture()
face = Face(decay=10)
timer = Timer()
key = 0

shift = [0, 0, -100]
fig = plt.figure()

while True:
    success, webcam_img = cap.read()
    if success:
        webcam_img = cv.flip(webcam_img, 1)
        webcam_gray = cv.cvtColor(webcam_img, cv.COLOR_BGR2GRAY)
        if timer.frame % 1 == 0:
            face.detect(webcam_img)
        face.draw(webcam_gray)

        # cv.imshow('Webcam', webcam_img)
        cv.imshow('Gray', webcam_gray)

        # ==== MATPLOT ====
        pixelnum = webcam_gray.shape[0] * webcam_gray.shape[1]
        binsnum = 25
        # print(pixelnum)

        fig.clear(True)
        hist = plt.hist(webcam_gray.flatten(), bins=binsnum, density=True)
        plt.ylim([0, 1 / 50])
        fig.canvas.draw()

        img = np.fromstring(fig.canvas.tostring_rgb(), dtype=np.uint8, sep='')
        img = img.reshape(fig.canvas.get_width_height()[::-1] + (3,))
        # img is rgb, convert to opencv's default bgr
        # img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
        cv.imshow("plot",img)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break

    print(f'fps: {timer.tick():.0f}')


cap.release()
cv.destroyAllWindows()
