from ast import main, mod
import cv2
import time
import mediapipe as mp

from HandTrackingModule import HandDetector as hd

pTime = 0 #previous time
cTime = 0 #current time

cap = cv2.VideoCapture(1)

detector = hd()


while True:
    success, img = cap.read()
    img = detector.findHands(img=img)
    lmlist = detector.findPosition(img)
    if len(lmlist):
        print(lmlist[4]) # passing in landmarknumber

    cTime = time.time()
    fps = 1/(cTime - pTime) #FPS, or Frames Per Second, is a measure of the rate at which a computer video game can produce and render frames. Generally, the higher the FPS number, the smoother and more engaging gameplay will be for users.
    pTime = cTime

    cv2.putText(img, str(int(fps)), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), 5)
    # print('fps is {}'.format(fps))
    cv2.imshow("Image", img)

    if cv2.waitKey(1) & 0xFF==ord("q"): #to stop the process when q is pressed
        break #https://stackoverflow.com/questions/46821936/open-cv-close-camera

cv2.destroyAllWindows()