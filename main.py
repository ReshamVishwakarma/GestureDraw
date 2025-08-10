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