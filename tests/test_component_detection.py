import functools
import glob
import numpy as np
import os

import cv2

import src.utils as utils
from src.old_etl.processor.component_detection import *

def skip_frame(capture: cv2.VideoCapture, frame_no: int, df: int):
    frame_no += df
    capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
    return frame_no


def show_video(capture: cv2.VideoCapture):
    frame_no = 0
    SPEED = 10
    while True:
        # for _ in range(SPEED - 1):
        #     capture.read()
        # else:
        #     _, frame = capture.read()
        #     frame_no += SPEED
        
        n_frames = 1
        capture.set(cv2.CAP_PROP_POS_FRAMES, frame_no + SPEED - n_frames)
        frame = np.uint8(np.average([capture.read()[1] for _ in range(n_frames)], axis=0))
        # _, frame = capture.read()
        frame_no = capture.get(cv2.CAP_PROP_POS_FRAMES)

        func_args = [
            (component_detection, (frame, 'logo')),
            (set_detection, (frame, 'set-1')),
            (score_detection, (frame, 'set-1-score', 12.0)),
            (score_detection_ocr, (frame, 'set-1-A')),
            (set_detection, (frame, 'set-2')),
            (score_detection, (frame, 'set-2-score', 12.0)),
            (set_detection, (frame, 'set-3')),
            (score_detection, (frame, 'set-3-score', 12.0)),
            (winner_detection, (frame,)),
        ]
        flags = [func(*arg) for func, arg in func_args]
        print(f'frame: {frame_no},', f'{(frame_no/VIDEO_FPS):.2f}s')
        print(flags)
        
        try:
            # condition_map = np.average(frame, axis=-1) < 150
            # frame[condition_map] = (0, 0, 0)
            for l, t, r, b in CROP_BOX.values():
                frame = cv2.rectangle(frame, (l, t), (r, b), (0, 0, 255), 1)
            cv2.imshow('title', frame)
        except:
            pass

        keycode = cv2.waitKey(1)
        if keycode == ord('q'):
            break
        elif keycode == ord(']'):
            frame_no = skip_frame(capture, frame_no, 2000)
        elif keycode == ord('['):
            frame_no = skip_frame(capture, frame_no, -2000)


def main():
    videos = glob.glob('videos/videos/*.mp4')
    cv2.namedWindow('title')
    cv2.setMouseCallback('title', utils.mouse_callback)
    for video_path in videos[0:2]:
        print(video_path)
        capture_instance = cv2.VideoCapture(video_path)
        show_video(capture_instance)



if __name__ == '__main__':
    main()