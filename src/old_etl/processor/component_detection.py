import functools
import numpy as np
import os

import cv2

import src.utils as utils
import src.old_etl.processor.ocr as OCR

VIDEO_FPS = 30
FILE_PATH = os.path.join('src', 'processor', 'component')
# tuple: (file-name, crop(left-top-right-bottom))
COMPONENT = {
    'match-bottom': 'match-bottom.png',
    'logo': 'on-game-logo.jpg',
}
CROP_BOX = {
    'match-bottom': (196, 655, 1084, 686),
    'logo': (202, 42, 240, 80),
    'set-1': (411, 45, 434, 80),
    'set-2': (440, 45, 463, 80),
    'set-3': (469, 45, 492, 80),
    'set-1-score': (413, 45, 432, 80),
    'set-1-A': (413, 45, 432, 58),
    'set-1-B': (413, 67, 432, 80),
    'set-2-score': (442, 45, 461, 80),
    'set-2-A': (442, 45, 461, 58),
    'set-2-B': (442, 67, 461, 80),
    'set-3-score': (471, 45, 490, 80),
    'set-3-A': (471, 45, 490, 58),
    'set-3-B': (471, 67, 490, 80),
}
POINT = {
    'player-1-win': (54, 408),
    'player-2-win': (75, 408),
}
PREV_CROP = dict()

TEMP = {
    'set-1-score': []
}


@functools.cache
def get_component(file_name: str) -> cv2.Mat:
    file_path = os.path.join(FILE_PATH, file_name)
    return cv2.imread(file_path)


def component_detection(frame: cv2.Mat, name: str) -> bool:
    file_name = COMPONENT[name]
    template = get_component(file_name)

    left, top, right, bottom = CROP_BOX[name]
    cropped_frame = frame[top:bottom, left:right, :]

    res = cv2.matchTemplate(cropped_frame, template, cv2.TM_CCOEFF_NORMED)
    threshold = 0.9
    loc = np.where(res >= threshold)
    return len(loc[1]) != 0


def crop(frame, name):
    left, top, right, bottom = CROP_BOX[name]
    cropped_frame = frame[top:bottom, left:right, :]
    return cropped_frame


def set_detection(frame, name):
    bgr_mean = np.mean(crop(frame, name), axis=(0, 1)).reshape((3,))
    m, v = np.mean(bgr_mean), np.var(bgr_mean)
    # print(bgr_mean)
    # print(m, v)
    if v < 100 and 60 < m and m < 110:
        return True
    else:
        return False

def score_detection(frame, name, threshold):
    prev = PREV_CROP.get(name, None)
    cropped = crop(frame, name)
    # cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # cropped = cv2.threshold(cropped, 60, 255, cv2.THRESH_BINARY)[1]
    # cropped = cv2.morphologyEx(cropped, cv2.MORPH_OPEN, np.ones((3, 3), np.uint8))
    # cropped = cv2.normalize(cropped, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX)
    # cropped = cv2.GaussianBlur(cropped, (5, 5), 0)
    cv2.imshow(name, cropped)
    if prev is None:
        PREV_CROP[name] = cropped
        return False
    # calculate difference between current and previous crop as MSE
    diff_image = cv2.absdiff(cropped, prev)
    diff_mse = np.mean(np.power(diff_image, 2), axis=(0, 1, 2))
    # print(diff_mse)
    if name == 'set-1-A' or name == 'set-1-B':
        TEMP['set-1-score'].append(diff_mse)
    # if flag:
    #     cv2.imshow('temp', diff_image)
    #     pass
    # cv2.imshow('temp__', diff_image)
    PREV_CROP[name] = cropped
    # threshold for naive = 12.0
    flag = diff_mse > threshold
    return flag

# score-detection alike function using set-n-A and set-n-B to detect
def score_detection_tweak(frame, name_a, name_b, threshold=50.0):
    return score_detection(frame, name_a, threshold) or score_detection(frame, name_b, threshold)


# return score from cropped frame by pytesseract
def score_detection_ocr(frame, name):
    cropped = crop(frame, name)
    cropped = cv2.cvtColor(cropped, cv2.COLOR_BGR2GRAY)
    # add border to prevent OCR from detecting text on border
    # value = mean of each pixel value
    border_value = np.average(cropped, axis=(0, 1))
    cropped = cv2.copyMakeBorder(cropped, 1, 1, 1, 1, cv2.BORDER_CONSTANT, value=border_value)
    cv2.imshow(name, cv2.resize(cropped, (0, 0), fx=5, fy=5))
    return OCR.text_from_img(cropped)


def winner_detection(frame):
    bgr_player1 = frame[POINT['player-1-win']]
    bgr_player2 = frame[POINT['player-2-win']]
    yellowish = lambda p: -int(p[0]) + int(p[1]) + int(p[2])
    if yellowish(bgr_player1) > yellowish(bgr_player2):
        return True
    else:  
        return False