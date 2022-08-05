# play video from a file, if i press space, crop frame and save it to a file

import functools
import glob
import itertools
import numpy as np
import os

import cv2

import src.etl.transform.feature_extract.utils as feutils
import src.utils as utils
import src.config as config


def show_video(capture: cv2.VideoCapture):
    frame_no = capture.set(cv2.CAP_PROP_POS_FRAMES, 10000)
    for _ in itertools.count():
        for _ in range(10):
            _, frame = capture.read()
        cv2.imshow('title', frame)
        frame_no = capture.get(cv2.CAP_PROP_POS_FRAMES)

        keycode = cv2.waitKey(1)
        if keycode == ord('q'):
            break
        elif keycode == ord(' '):
            name = 'score-b'
            frame = feutils.crop(frame, name)
            cv2.imwrite(f'{config.CONDITION_IMAGE_FILE_PATH}/{int(frame_no)}-{name}.png', frame)
        elif keycode == ord('s'):
            cv2.imwrite(f'dummy/{int(frame_no)}.png', frame)
        elif keycode == ord(']'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 10000)
        elif keycode == ord('['):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 10000)
        elif keycode == ord('}'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + 1000)
        elif keycode == ord('{'):
            capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no - 1000)



def main():
    videos = glob.glob(os.path.join(config.VIDEOS_PATH, '*.mp4'))
    print(videos)
    cv2.namedWindow('title')
    for video_path in videos[0:4]:
        print(video_path)
        capture_instance = cv2.VideoCapture(video_path)
        show_video(capture_instance)


if __name__ == '__main__':
    main()