import glob
import itertools
import numpy as np
import os

import cv2
import tqdm

import src.config as config
import src.etl.transform.feature_extract.feature_extract as fe
import src.etl.transform.event.event_detect as ed


def extract_feature(frame: cv2.Mat) -> tuple[tuple]:
    '''
    extract_features from frame
    PARAMETER:
        frame: cv2.Mat - frame to extract features from
    RETURN:
        tuple(tuple) - features
    '''
    return (
        fe.is_logo_on(frame),
        fe.get_score_data(frame),
        fe.get_scored_player(frame),
    )


def util_rangeplay(capture: cv2.VideoCapture, start_frame: int, end_frame: int):
    '''
    play video with range of frames
    PARAMETER:
        capture: cv2.VideoCapture - video capture instance
    '''
    frame_no = capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    while True:
        keycode = cv2.waitKey(1)
        if keycode == ord('q'):
            break
        elif keycode == ord(' '):
            print(frame_no)
            cv2.waitKey(0)
        
        _, frame = capture.read()
        cv2.imshow('title', frame)
        frame_no = capture.get(cv2.CAP_PROP_POS_FRAMES)
        if frame_no >= end_frame:
            capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)


def annotate_video(capture: cv2.VideoCapture) -> list[tuple[int, str]]:
    '''
    annotate video to list of events.
    1. extract features from each frame
    2. find event from change of features. 
    '''
    start_frame = 0
    end_frame = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    skip_frames = 10

    sequence = []

    frame_no = capture.set(cv2.CAP_PROP_POS_FRAMES, start_frame)
    for frame_no in tqdm.tqdm(range(start_frame, end_frame, skip_frames)):
        if skip_frames >= 10:
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        else:
            for _ in range(skip_frames - 1):
                capture.read()
        frame = capture.read()[1]
        features = extract_feature(frame)
        sequence.append((frame_no, features))
    
    events = ed.event_detection(sequence)

    return events


if __name__ == '__main__':
    videos = glob.glob(os.path.join(config.VIDEOS_PATH, '*.mp4'))
    print(videos)
    # cv2.namedWindow('title')
    for video_path in videos[0:1]:
        print(video_path)
        capture_instance = cv2.VideoCapture(video_path)
        annotate_video(capture_instance)