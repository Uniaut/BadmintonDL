import functools
import os
import cv2
import pickle


PICKLE_CACHE_PATH = os.path.join('cache')

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('[MOUSE] pos x:', x ,' y:', y)
