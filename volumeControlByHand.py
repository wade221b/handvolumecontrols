import cv2
import time
import mediapipe as mp
import HandTrackingModule as htm

cap = cv2.VideoCapture(1)

# wCam, hCam = 640, 480 #to set camera width
wCam, hCam = 1280, 720 #set a bigger camera

detector = htm.HandDetector(detectionConfidence=0.7)

cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0 #previous time
cTime = 0 #current time

while True:
    success, img = cap.read()

    img = detector.findHands(img=img)

    lmlist = detector.findPosition(img, draw=False)
    # print(lmlist ) #list of all the legends

    if len(lmlist):
        print('thumb endpoint ', lmlist[4])
        print('index finger endpoint ',lmlist[8])

        x1, y1 = lmlist[4][1],  lmlist[4][2]
        x2, y2 = lmlist[8][1],  lmlist[8][2]

    cTime = time.time()
    fps = 1/(cTime - pTime) #FPS, or Frames Per Second, is a measure of the rate at which a computer video game can produce and render frames. Generally, the higher the FPS number, the smoother and more engaging gameplay will be for users.
    pTime = cTime

    cv2.putText(img, str(int(fps)), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), 5) #doesnt work
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord("q"): #to stop the process when q is pressed
        break #https://stackoverflow.com/questions/46821936/open-cv-close-camera