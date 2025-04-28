import cv2
import time
import mediapipe as mp

cap = cv2.VideoCapture(1)

mpHands = mp.solutions.hands

hands = mpHands.Hands(False)
#static_image_mode => true : whole time detects a hand. makes code slow as continuously tracking
#                     false : detects and if found > some confidence level, tracks
# max_num_hands=2,
# model_complexity=1,
# min_detection_confidence=0.5,
# min_tracking_confidence=0.5)
#only uses RGB images. hence the image from camera has to first be converted

mpDraw = mp.solutions.drawing_utils 
#function to draw line between the 21 points.

while True:
    success, img = cap.read()

    #to send RGB image to the hands. for that first need to convert 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #the image from camera has to first be converted
    results = hands.process(imgRGB)

    print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: #draw lines for each hand ditected
            mpDraw.draw_landmarks(img, handLms) #because we are displaying on the original image, we pass this and not the RGB image

    cv2.imshow("Image", img)
    # cv2.waitKey(1) #basic code to run a webcam-

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break #https://stackoverflow.com/questions/46821936/open-cv-close-camera

cv2.destroyAllWindows()