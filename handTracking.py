import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(1)

while True:
    success, img = cap.read()

    cv2.imshow("Image", img)
    cv2.waitKey(1) #basic code to run a webcam