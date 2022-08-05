import functools
import glob
import itertools
import numpy as np
import os

import cv2

import src.utils as utils
import src.config as config


def show_video(capture: cv2.VideoCapture):
    frame_no = capture.set(cv2.CAP_PROP_POS_FRAMES, 10000)
    for _ in itertools.count():
        for _ in range(20):            _, frame = capture.read()
        cv2.imshow('title', frame)
        frame_no = capture.get(cv2.CAP_PROP_POS_FRAMES)

        keycode = cv2.waitKey(1)
        if keycode == ord('q'):
            break
        elif keycode == ord(' '):
            print(frame_no)
            cv2.waitKey(0)
        elif keycode == ord(']'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 10000)
        elif keycode == ord('['):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 10000)
        elif keycode == ord('}'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 1000)
        elif keycode == ord('{'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 1000)



def annotation_mode(capture: cv2.VideoCapture):
    frame_no = capture.set(cv2.CAP_PROP_POS_FRAMES, 100000)
    frame = capture.read()[1]
    cv2.imshow('title', frame)
    for _ in itertools.count():
        frame_no = capture.get(cv2.CAP_PROP_POS_FRAMES)

        keycode = cv2.waitKey(1)
        if keycode == ord('q'):
            break
        elif keycode == ord(']'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 20 - 1)
            print(frame_no)
            frame = capture.read()[1]
        elif keycode == ord('['):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 20 - 1)
            print(frame_no)
            frame = capture.read()[1]
        elif keycode == ord('}'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 10000 - 1)
            frame = capture.read()[1]
        elif keycode == ord('{'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 10000 - 1)
            frame = capture.read()[1]
        else:
            continue
        cv2.imshow('title', frame)




def main():
    videos = glob.glob(os.path.join(config.VIDEOS_PATH, '*.mp4'))
    print(videos)
    cv2.namedWindow('title')
    cv2.setMouseCallback('title',utils.mouse_callback)  
    for video_path in videos[0:1]:
        print(video_path)
        capture_instance = cv2.VideoCapture(video_path)
        annotation_mode(capture_instance)


if __name__ == '__main__':
    main()