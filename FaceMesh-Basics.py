import cv2
import mediapipe as mp
import time
import numpy as np


mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_face_mesh = mp.solutions.face_mesh

drawing_spec = mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
FaceMesh = mp_face_mesh.FaceMesh(max_num_faces=1, refine_landmarks=True, min_detection_confidence=0.5,
                            min_tracking_confidence=0.5)
cap = cv2.VideoCapture(0)

pTime = 0


while True:
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      continue

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = FaceMesh.process(image)

    # Draw the face mesh annotations on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    if results.multi_face_landmarks:
      for face_landmarks in results.multi_face_landmarks:
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION,
            landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_CONTOURS,
            landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES,
            landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())

        for id,lm in enumerate(face_landmarks.landmark):
            #print(lm)#Posotion landmark x,y and z
            ih, iw, ic = image.shape # get shape of original frame
            x,y,z = int(lm.x*iw), int(lm.y*ih), int(lm.z*ic)
            print(id,x,y,z)

#############################################################
        ########-Hintergrund-bilder-########
        # Extract and draw pose on plain white image
        h, w, c = image.shape  # get shape of original frame
        opImg = np.zeros([h, w, c])  # create blank image with original frame size
        opImg.fill(0)  # set Black background. put 0 if you want to make it black and 255 if you want it white

        # draw extracted pose on black white image
        mp_drawing.draw_landmarks(image=opImg, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_TESSELATION,
                                  landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())
        mp_drawing.draw_landmarks(image=opImg, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_CONTOURS,
                                  landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style())
        mp_drawing.draw_landmarks(image=opImg, landmark_list=face_landmarks, connections=mp_face_mesh.FACEMESH_IRISES,
                                  landmark_drawing_spec=None, connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_iris_connections_style())

        cv2.imshow('Extracted Face', opImg)

    ######-Time-##########
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
##########################################

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Face Mesh', image)
    if cv2.waitKey(5) & 0xFF == 27:
      break
cap.release()