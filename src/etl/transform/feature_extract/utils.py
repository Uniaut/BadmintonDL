import functools
import glob
import numpy as np
import os

import cv2

import src.utils as utils
import src.config as config


@functools.cache
def get_template(file_name: str) -> cv2.Mat:
    '''
    load component image from file_name and cache it
    PARAMETERS:
        file_name: str - file name of template
    '''
    file_path = os.path.join(config.CONDITION_IMAGE_FILE_PATH, file_name)
    return cv2.imread(file_path)


'''
crop area alias
* (left, top, right, bottom)
        A B C
LOGO
        D E F
'''
CROP_AREA = {
    'logo': (202, 42, 240, 80),
    'score-a': (413, 45, 432, 58),
    'score-b': (442, 45, 461, 58),
    'score-c': (471, 45, 490, 58),
    'score-d': (413, 66, 432, 79),
    'score-e': (442, 66, 461, 79),
    'score-f': (471, 66, 490, 79),
}


def crop(frame, name):
    left, top, right, bottom = CROP_AREA[name]
    cropped_frame = frame[top:bottom, left:right, :]
    return cropped_frame


def mean(image: cv2.Mat) -> float:
    return np.mean(image)


def mse(img1: cv2.Mat, img2: cv2.Mat):
    img1, img2 = np.float16(img1), np.float16(img2)
    mse = np.mean(np.square(img1 - img2))
    return mse


def mse_from_template_and_frame(frame: cv2.Mat, crop_area_key: str, template_name: str):
    '''
    get mse from template file and cropped frame
    PARAMETERS:
        crop_area_key: str - key string of CROP_AREA
        template_name: str - file name of template
        frame: cv2.Mat - frame to compare
    '''
    assert(crop_area_key in CROP_AREA)
    assert(os.path.exists(config.CONDITION_IMAGE_FILE_PATH))

    cropped = crop(frame, crop_area_key)
    cropped = cv2.GaussianBlur(cropped, (3, 3), 0)
    template = get_template(template_name)
    template = cv2.GaussianBlur(template, (3, 3), 0)
    return mse(cropped, template)
