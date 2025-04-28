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

pTime = 0 #previous time
cTime = 0 #current time

while True:
    success, img = cap.read()

    #to send RGB image to the hands. for that first need to convert 
    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  #the image from camera has to first be converted
    results = hands.process(imgRGB)

    # print(results.multi_hand_landmarks)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks: #draw lines for each hand ditected
            for id, lm in enumerate(handLms.landmark): #21 values would be printed. those are the landmark as documentd in HandLandmark.png

                h, w, c = img.shape
                cx, cy = int(lm.x * w ), int(lm.y*h) #position of centre
                print(id, cx, cy)

                if id == 0:
                    cv2.circle(img, (cx, cy), 20, (255, 0, 255), cv2.FILLED)
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS) #because we are displaying on the original image, we pass this and not the RGB image
            #mpHands.HAND_CONNECTIONS draws the connections between those points
    cv2.imshow("Image", img)
    # cv2.waitKey(1) #basic code to run a webcam-

    cTime = time.time()
    fps = 1/(cTime - pTime) #FPS, or Frames Per Second, is a measure of the rate at which a computer video game can produce and render frames. Generally, the higher the FPS number, the smoother and more engaging gameplay will be for users.
    pTime = cTime

    cv2.putText(img, str(int(fps)), (100, 70), cv2.FONT_HERSHEY_COMPLEX, 3, (255,0, 255), 20) #doesnt work
    # print('fps is {}'.format(fps))

    if cv2.waitKey(1) & 0xFF==ord("q"): #to stop the process when q is pressed
        break #https://stackoverflow.com/questions/46821936/open-cv-close-camera

cv2.destroyAllWindows()