import cv2
import mediapipe as mp
import os
import time
import numpy as np

#Webcam initialization
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 1000)
cap.set(10, 150)

#Mediapipe Hand
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpdraw = mp.solutions.drawing_utils

pasttime = 0

folder = 'colors'
mylist = os.listdir(folder)
overlist = []

#BGR color palette
color_list = [
    (0, 0, 0),          #Eraser - Black
    (255, 0 , 255),     #Pink
    (0, 0, 255),        #Red
    (0, 255, 0),        #Green        
    (255, 0 , 0),       #Blue
    (0, 255, 255),      #Yellow
    (0, 127, 255),      #Orange
    (255, 0, 127)       #Purple

]

for img_name in mylist:
    image = cv2.imread(f'{folder}/{img_name}')
    overlist.append(image)

header = overlist[0]
col = color_list[0]    

xp, yp = 0, 0
canvas = np.zeros((480, 640, 3), np.uint8)

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)
    
    img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = hands.process(img)
    landmark = []

    if results.multi_hand_landmarks:
        for hn in results.multi_hand_landmarks:
            for id, lm in enumerate(hn, landmark):
                h, w, c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                landmark.append([id, cx, cy])

            mpdraw.draw_landmarks(frame, h, mpHands.HAND_CONNECTIONS)    

    if len(landmark) != 0:
        x1, y1 = landmark[8][1], landmark[8][2]
        x2, y2 = landmark[12][1], landmark[12][2]

        #Selection Mode
        if landmark[8][2] < landmark[6][2] and landmark[12][2] < landmark[10][2]:
            xp, yp = 0, 0
            if y1 < 100:
                slot_width = 640 // len(overlist)
                for i in range(len(overlist)):
                    if i in range(len(overlist)):
                        if i * slot_width < x1 < (i + 1) * slot_width:
                            header = overlist[i]
                            col = color_list[i % len(color_list)]
            cv2.rectangle(frame, (x1, y1), (x2, y2), col, cv2.FILLED)


                            
        #Drawing Mode
        elif landmark[8][2] < landmark[6][2]:
            if xp == 0 and yp == 0:
                xp, yp = x1, y1
                if col == (0, 0, 0):
                    cv2.line(frame, (xp, yp), (x1, y1), col, 75)
                    cv2.line(canvas, (xp, yp), (x1, y1), col, 75)
                else:
                    cv2.line(frame, (xp, yp), (x1, y1), col, 13)
                    cv2.line(canvas, (xp, yp), (x1, y1), col, 13)
                xp, yp = x1, y1        

    #Blend Canvas
    imgGray = cv2.cvtColor(canvas, cv2.COLOR_BGR2GRAY)
    _, imgInv = cv2.threshold(imgGray, 50, 255, cv2.THRESH_BINARY_INV)
    imgInv = cv2.cvtColor(imgInv, cv2.COLOR_GRAY2BGR)
    frame = cv2.bitwise_and(frame, imgInv)
    frame = cv2.bitwise_or(frame, canvas)

    frame[0: 100, 0: 640] = header


    #FPS
    ctime = time.time()
    fps = 1/(ctime - pasttime)
    pasttime = ctime
    cv2.putText(frame, f'FPS: {int(fps)}', (490, 150), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 0), 3)

    #Mode and Color Indicator
    mode_text = "Drawing" if xp != 0 else "Selection"
    cv2.putText(frame, f'Mode: {mode_text}', (10, 450), cv2.FONT_HERSHEY_SIMPLEX, 1, col, 2)

    cv2.imshow('cam', frame)
    cv2.imshow('canvas', canvas)

    