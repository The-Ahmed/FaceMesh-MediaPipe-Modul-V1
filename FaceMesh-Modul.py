import cv2
import mediapipe as mp
import time
import numpy as np

class FaceMeshDetector():


    def __init__(self, staticMode=False, maxFaces=1, refLandmarks=False,
                 minDetectionCon=0.5, minTrackCon=0.5):

        self.maxFaces = maxFaces
        self.refLandmarks = refLandmarks
        self.staticMode = staticMode
        self.minTrackCon = minTrackCon
        self.minDetectionCon = minDetectionCon

        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.mp_face_mesh = mp.solutions.face_mesh
        self.drawing_spec = self.mp_drawing.DrawingSpec(thickness=1, circle_radius=1)
        self.FaceMesh = self.mp_face_mesh.FaceMesh(self.staticMode, self.maxFaces, self.refLandmarks,
                                                   self.minDetectionCon, self.minTrackCon)


    def findFaceMesh(self, image, draw=True):

# To improve performance, optionally mark the image as not writeable to
    # pass by reference.
        #self.image.flags.writeable = False
        self.imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        self.results = self.FaceMesh.process(self.imageRGB)

    # Draw the face mesh annotations on the image.
        #self.image.flags.writeable = True
        #self.image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        if self.results.multi_face_landmarks:

            for face_landmarks in self.results.multi_face_landmarks:
                if draw:
                    self.mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=self.mp_face_mesh.FACEMESH_TESSELATION,
                                            landmark_drawing_spec=None, connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_tesselation_style())
                    self.mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=self.mp_face_mesh.FACEMESH_CONTOURS,
                                            landmark_drawing_spec=None, connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_contours_style())
                    #self.mp_drawing.draw_landmarks(image=image, landmark_list=face_landmarks, connections=self.mp_face_mesh.FACEMESH_IRISES,
                                            #landmark_drawing_spec=None, connection_drawing_spec=self.mp_drawing_styles.get_default_face_mesh_iris_connections_style())

                face = []
                for id,lm in enumerate(face_landmarks.landmark):
                    #print(lm)#Posotion landmark x,y and z
                    ih, iw, ic = image.shape # get shape of original frame
                    x,y,z = int(lm.x*iw), int(lm.y*ih), int(lm.z*ic)
                    #ID Face Detection
                    #cv2.putText(image, str(id), (x, y), cv2.FONT_HERSHEY_PLAIN, 0.5, (0, 255, 0), 1)

                    #print(id,x,y,z)
                    face.append([x,y])
        #faces.append(face)
            return image, face


def main():

    cap = cv2.VideoCapture(0)
    pTime = 0
    detector = FaceMeshDetector(maxFaces=1)
    while True:
        success, image = cap.read()
        image, face = detector.findFaceMesh(image) # if I need only ID Nommer whrite image, face = detector.findFaceMesh(image, False)
        if len(face) != 0:
            print(face[0])

    ######-Time-##########
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime
        cv2.putText(image, f'FPS: {int(fps)}', (20, 70), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        ##########################################

    # Flip the image horizontally for a selfie-view display.
        cv2.imshow('Image', image)
        cv2.waitKey(1)
        #if cv2.waitKey(5) & 0xFF == 27:
            #break
    #cap.release()

if __name__ == "__main__":
    main()