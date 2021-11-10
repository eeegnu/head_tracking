
import cv2 as cv
import numpy as np
from icecream import ic

from face import Face
from room import Room
from utils import Timer, setup_capture, add_text
from constants import ROOM_WIDTH, ROOM_HEIGHT, step_size, scalez


cap = setup_capture()
face = Face()
room = Room()
timer = Timer()
key = 0

shift = [0, 0, -100]

while True:
    success, webcam_img = cap.read()
    if success:
        webcam_img = cv.flip(webcam_img, 1)
        if timer.frame % 2 == 0:
            face.detect(webcam_img)
        face.draw(webcam_img)
        camera = face.coordinates()
        camera[0] *= ROOM_WIDTH
        camera[1] *= ROOM_HEIGHT
        camera[2] = scalez * camera[2]
        camera = (np.array(camera) + np.array(shift)).tolist()

        room_img = np.zeros((ROOM_HEIGHT, ROOM_WIDTH, 3), np.uint8)
        room.draw(room_img, camera)

        webcam_scaled = webcam_img[::3, ::3]
        room_img[-webcam_scaled.shape[0]:, -webcam_scaled.shape[1]:] = webcam_scaled
        add_text(room_img, f'fps: {timer.fps:.0f}', (0, 30))
        add_text(room_img, f'xyz: {list(map(round, camera))}', (ROOM_WIDTH-370, 30))
        add_text(room_img, f'key pressed: {chr(key).upper()}', (0, ROOM_HEIGHT-10))
        cv.imshow('Room', room_img)
        # cv.imshow('Webcam', webcam_scaled)

        key = cv.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        elif key == ord('w'):
            shift[2] -= step_size
        elif key == ord('s'):
            shift[2] += step_size
        elif key == ord('a'):
            shift[0] -= step_size
        elif key == ord('d'):
            shift[0] += step_size
        elif key == ord('r'):
            shift[1] -= step_size
        elif key == ord('f'):
            shift[1] += step_size

    print(f'fps: {timer.tick():.0f}')


cap.release()
cv.destroyAllWindows()
