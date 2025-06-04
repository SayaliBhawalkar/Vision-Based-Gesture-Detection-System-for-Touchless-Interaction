
from unittest import result
import cv2
from matplotlib import image
import numpy as np
import cv2
import mediapipe as mp
import pyautogui
import math
from enum import IntEnum
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from google.protobuf.json_format import MessageToDict
import screen_brightness_control as sbcontrol
import pyttsx3
import speech_recognition as sr
from datetime import date
import time
import webbrowser
import datetime
from pynput.keyboard import Key, Controller
import pyautogui
import sys
import os
from os import listdir
from os.path import isfile, join
import smtplib
import wikipedia
import Gesture_Controller
#import Gesture_Controller_Gloved as Gesture_Controller
import app
from threading import Thread
import eel
import os
from queue import Queue
import numpy as np
import cv2
import cv2.aruco as aruco
import os
import glob
import math
import pyautogui
import time
import Gesture_Controller as handmajor
from Gesture_Controller_Gloved import mp_drawing, mp_hands
gest_name = handmajor.get_gesture()
Controller.handle_controls(gest_name, handmajor.hand_result)
                    
for hand_landmarks in result.multi_hand_landmarks:
                        mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
else:
                    Controller.prev_hand = None
cv2.imshow('Gesture Controller', image)