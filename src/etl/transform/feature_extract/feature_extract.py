'''
feature_extact.py

all functions return tuple of (feature, extra-data-for-log)
any can be used as log message
'''
import glob
import itertools
import numpy as np
import os

import cv2
import pytesseract

import src.config as config
import src.etl.transform.feature_extract.utils as feutils


# check is cropped frame logo
def is_logo_on(frame: cv2.Mat) -> tuple[bool, float]:
    '''
    check is cropped frame logo
    PARAMETERS:
        frame: cv2.Mat - frame to check
    '''
    result = feutils.mse_from_template_and_frame(frame, 'logo', 'logo.png')
    return (result < config.IS_LOGO_THRESHOLD, result)


def get_score_number(frame: cv2.Mat, area: str) -> tuple[int, tuple[float]]:
    '''
    get point score from frame and area alphabet
    PARAMETERS:
        frame: cv2.Mat - frame to check
        area: str - area alphabet
    RETURN:
        tuple(int, tuple(float, ...)) - point score and similarity of each template
    '''
    assert(area in ['score-a', 'score-b', 'score-c', 'score-d', 'score-e', 'score-f'])
    templates_id = list(map(str, range(31))) + ['_'] # ['0', '1', ... , '30', '_']
    scores = list(range(31)) + [0] # [0, 1, ... , 21, 0]
    
    result = [
        (score, feutils.mse_from_template_and_frame(frame, area, template_id + '.png'))
        for score, template_id in zip(scores, templates_id)
    ]
    return (max(result, key=lambda i: -i[1]), result)


def get_scored_player(frame: cv2.Mat) -> tuple[int, tuple[float, float]]:
    '''
    get scored player from frame
    PARAMETERS:
        frame: cv2.Mat - frame to check
    '''
    POINT1, POINT2 = (54, 408), (74, 408)
    bgr_player1 = frame[POINT1]
    bgr_player2 = frame[POINT2]
    yellowish = lambda p: -int(p[0]) + int(p[1]) + int(p[2])
    result1 = yellowish(bgr_player1)
    result2 = yellowish(bgr_player2)
    return (1 if result1 > result2 else 2, (result1, result2))


def get_score_data(frame: cv2.Mat) -> tuple[tuple[int, int, int], tuple[float, float]]:
    '''
    get game #, score # of each player with extra data
    PARAMETERS:
        frame: cv2.Mat - frame to check
        set: int - set to check
    '''
    data = {
        1: ('score-a', 'score-d'),
        2: ('score-b', 'score-e'),
        3: ('score-c', 'score-f'),
    }

    result = (0, 0, 0)
    # TODO: get score from each game #
    for game_num, areas in data.items():
        score1, score2 = get_score_number(frame, areas[0])[0], get_score_number(frame, areas[1])[0]
        if score1[1] > config.SCORE_AREA_VALIDITY_THRESHOLD or score2[1] > config.SCORE_AREA_VALIDITY_THRESHOLD:
            break
        else:
            result = (game_num, score1[0], score2[0])
    return (result, (score1[1], score2[1]))




# simple heuristic validation code
if __name__ == '__main__':
    # get point score from frames in dummy directory
    frames = glob.glob(os.path.join('dummy', '*.png'))
    for frame_path in frames:
        frame = cv2.imread(frame_path)
        print(frame_path)
        print(get_score_data(frame))
        print(get_scored_player(frame))
        print('b', get_score_number(frame, 'score-b'))
        print('e', get_score_number(frame, 'score-e'))
        print(is_logo_on(frame))
        cv2.imshow('frame', frame)
        cv2.waitKey(0)