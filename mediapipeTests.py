import cv2 as cv
import numpy as np
from icecream import ic
import mediapipe as mp

from face import Face
from room import Room
from utils import Timer, setup_capture, add_text
from constants import ROOM_WIDTH, ROOM_HEIGHT, step_size, scalez
import time

cap = setup_capture()
face = Face()
room = Room()
timer = Timer()
key = 0

shift = [0, 0, -100]
faceCentroids = []

#mostly just using the video cam part from: https://google.github.io/mediapipe/solutions/face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

with mp_face_mesh.FaceMesh(
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5) as face_mesh:

    while True:
        success, webcam_img = cap.read()
        if success:
            webcam_img.flags.writeable = False
            #webcam_img = cv.flip(webcam_img, 1)
            #if timer.frame % 1 == 0:
            #    start = time.time()
            #    face.detect(webcam_img)
            #    print(time.time() - start)
            #face.draw(webcam_img)

            results = face_mesh.process(webcam_img)
            webcam_img.flags.writeable = True
            if results.multi_face_landmarks:
                faceCentroid = [0,0,0]
                for facemesh in results.multi_face_landmarks:
                    for landmark in facemesh.landmark:
                        faceCentroid[0] += landmark.x
                        faceCentroid[1] += landmark.y
                        faceCentroid[2] += landmark.z
                    for i in range(3):
                        faceCentroid[i] /= len(facemesh.landmark)
                    faceCentroids.append(faceCentroid)
                    print(faceCentroid)

                    mp_drawing.draw_landmarks(
                        image=webcam_img,
                        landmark_list=facemesh,
                        connections=mp_face_mesh.FACEMESH_TESSELATION,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_tesselation_style())
                    mp_drawing.draw_landmarks(
                        image=webcam_img,
                        landmark_list=facemesh,
                        connections=mp_face_mesh.FACEMESH_CONTOURS,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_contours_style())
                    mp_drawing.draw_landmarks(
                        image=webcam_img,
                        landmark_list=facemesh,
                        connections=mp_face_mesh.FACEMESH_IRISES,
                        landmark_drawing_spec=None,
                        connection_drawing_spec=mp_drawing_styles
                        .get_default_face_mesh_iris_connections_style())
            webcam_img = cv.flip(webcam_img, 1)

            camera = faceCentroid
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
