import cv2
import mediapipe as mp
import os
import time
import numpy as mp

#Webcam initialization
cap = cv2.VideoCapture(0)
cap.set(3, 640)
cap.set(4, 1000)
cap.set(10, 150)

