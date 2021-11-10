
import cv2 as cv

RED   = (  0,   0, 255)
GREEN = (  0, 255,   0)
WHITE = (255, 255, 255)

CAM_WIDTH, CAM_HEIGHT = 1280, 720
ROOM_WIDTH, ROOM_HEIGHT = 1800, 1070

scalez = 50
screenz = -4 * scalez  # where to project to
step_size = 50

font        = cv.FONT_HERSHEY_SIMPLEX
fontScale   = 1
fontColor   = GREEN
lineType    = 2