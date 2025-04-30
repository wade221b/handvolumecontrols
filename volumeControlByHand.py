import math
import cv2
import time
import mediapipe as mp

import HandTrackingModule as htm
import DeviceVolumeControl as dvc

cap = cv2.VideoCapture(1)
vol = dvc.DeviceVolumeControlCrude()

# wCam, hCam = 640, 480 #to set camera width
wCam, hCam = 1280, 720 #set a bigger camera

detector = htm.HandDetector(detectionConfidence=0.7)

cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0 #previous time
cTime = 0 #current time

def getVolume(dist):
    #considering 30 is zero and 250 is full volume, 
    #250-30 is the range that would be plotted against the 100% volume barrier
    #basic maths

    disttoplot = dist - 30
    finalvolume = (disttoplot*100)//220

    if finalvolume < 0:
        return 0
    elif finalvolume >100:
        return 100
    return int(finalvolume)


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
        pt1 = (x1, y1)
        pt2 = (x2, y2)

        centreX, centreY = (x1+x2)//2, (y1+y2)//2

        cv2. circle(img, (x1, y1), 15, (255, 20, 49), cv2.FILLED, 5)
        cv2. circle(img, (x2, y2), 15, (255, 20, 49), cv2.FILLED, 5)
        cv2.line(img, (x1, y1),  (x2, y2), cv2.FILLED)

        volume = 0
        distBetweenFingers = math.dist(pt1, pt2)
        print(distBetweenFingers)

        if distBetweenFingers <= 30:
            volume = getVolume(30)
            cv2.circle(img, (centreX, centreY), 15, (0, 255, 0), cv2.FILLED)
            vol.mute_system()
        elif distBetweenFingers >= 250:
            volume = getVolume(250)
            vol.set_system_volume(100)
        else:
            volume = getVolume(distBetweenFingers)
            vol.set_system_volume(volume)
            # pass
        strin = "finger dist {} and vol = {} ".format(int(distBetweenFingers), volume)
        cv2.putText(img, strin, (100, 70), cv2.FONT_HERSHEY_COMPLEX, 1, (255,0, 255), 5) 

        # cv2.putText(img, str(int(distBetweenFingers), volume), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), 5) 

    cTime = time.time()
    fps = 1/(cTime - pTime) #FPS, or Frames Per Second, is a measure of the rate at which a computer video game can produce and render frames. Generally, the higher the FPS number, the smoother and more engaging gameplay will be for users.
    pTime = cTime

    # cv2.putText(img, str(int(distBetweenFingers)), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), 5) 
    
    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF==ord("q"): #to stop the process when q is pressed
        break #https://stackoverflow.com/questions/46821936/open-cv-close-camera