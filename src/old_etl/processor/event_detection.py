import glob
import numpy as np
from datetime import datetime

import cv2
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import tqdm

import src.utils as utils
from src.processor.component_detection import *

# constant of frequent integers
BEFORE_SET_1 = 15000
AFTER_SET_1 = 55000
SPEED: int = 50

def process_video(capture: cv2.VideoCapture):
    result = []
    length = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))
    print('video length:', length)
    capture.set(cv2.CAP_PROP_POS_FRAMES, BEFORE_SET_1)
    for frame_no in tqdm.tqdm(range(BEFORE_SET_1, AFTER_SET_1, SPEED)):
        for _ in range(SPEED - 1):
            capture.read()
        frame = capture.read()[1]
        # frame = np.uint8(
        #     np.average([capture.read()[1] for _ in range(SPEED)], axis=0)
        # )
        # _, frame = capture.read()
        cv2.imshow('', cv2.resize(frame.copy(), (0, 0), fx=0.1, fy=0.1))
        cv2.waitKey(1)

        func_args = [
            (component_detection, (frame, 'logo')),
            (set_detection, (frame, 'set-1')),
            (score_detection_tweak, (frame, 'set-1-A', 'set-1-B')),
            (set_detection, (frame, 'set-2')),
            (score_detection_tweak, (frame, 'set-2-A', 'set-2-B')),
            (set_detection, (frame, 'set-3')),
            (score_detection_tweak, (frame, 'set-3-A', 'set-3-B')),
            (winner_detection, (frame,)),
        ]
        flags = [func(*arg) for func, arg in func_args]
        result.append((frame_no, flags))
    
    cv2.destroyAllWindows()
    return result

FLAG_ON_GAME_LOGO = 0
FLAG_SET_1 = 1
FLAG_SET_1_SCORE = 2
FLAG_SET_2 = 3
FLAG_SET_2_SCORE = 4
FLAG_SET_3 = 5
FLAG_SET_3_SCORE = 6
FLAG_IS_WINNER_1 = 7


def add_events(last_event: dict, events: list, event_name: str, timestamp: int, content=None):
    # if last event != 0 and last event is near to this event, do not add this event
    if last_event[event_name] != -1 and last_event[event_name] + 40 > timestamp:
        return

    if last_event[event_name] != -1 and event_name in [
        'match-start',
        'set-1-start',
        'set-2-start',
        'set-3-start',
        'set-1-score',
        'set-2-score',
        'set-3-score'
    ]:

        return  
    
    events.append((event_name, timestamp, content))
    last_event[event_name] = timestamp


def catch_events(flags_seq):
    events = []
    prev_flags = []
    score = {
        'set-1-1': 0,
        'set-1-2': 0,
        'set-2-1': 0,
        'set-2-2': 0,
        'set-3-1': 0,
        'set-3-2': 0,
    }
    # timestamp of last called event
    last_event = {
        'set-1-start': -1,
        'set-1-winner-1': -1,
        'set-1-winner-2': -1,
        'set-1-score': -1,
        'set-2-start': -1,
        'set-2-winner-1': -1,
        'set-2-winner-2': -1,
        'set-2-score': -1,
        'set-3-start': -1,
        'set-3-winner-1': -1,
        'set-3-winner-2': -1,
        'set-3-score': -1,
    }
    for seq_idx, flag_set in enumerate(flags_seq):
        frame_no, flags = flag_set
        if seq_idx == 0:
            prev_temp_flags = flags
            continue

        prev_flags = prev_temp_flags
        prev_temp_flags = flags
        print(frame_no, prev_flags, '->', flags)
        if not prev_flags[FLAG_ON_GAME_LOGO] and flags[FLAG_ON_GAME_LOGO]:
            events.append(('match-start', frame_no))
            continue

        if flags[FLAG_SET_1]:
            if not prev_flags[FLAG_SET_1]:
                add_events(last_event, events, 'set-1-start', frame_no)
            elif flags[FLAG_SET_1_SCORE]:
                if flags[FLAG_IS_WINNER_1]:
                    score['set-1-1'] += 1
                    add_events(last_event, events, 'set-1-winner-1', frame_no)
                else:
                    score['set-1-2'] += 1
                    add_events(last_event, events, 'set-1-winner-2', frame_no)
        else:
            continue

        if flags[FLAG_SET_2]:
            if not prev_flags[FLAG_SET_2]:
                # add event of set-1 score
                add_events(last_event, events, 'set-1-score', frame_no, (score['set-1-1'], score['set-1-2']))
                add_events(last_event, events, 'set-2-start', frame_no)
            elif flags[FLAG_SET_2_SCORE]:
                if flags[FLAG_IS_WINNER_1]:
                    score['set-2-1'] += 1
                    add_events(last_event, events, 'set-2-winner-1', frame_no)
                else:
                    score['set-2-2'] += 1
                    add_events(last_event, events, 'set-2-winner-2', frame_no)
        else:
            continue

        if flags[FLAG_SET_3]:
            if not prev_flags[FLAG_SET_3]:
                # add event of set-2 score
                add_events(last_event, events, 'set-2-score', frame_no, (score['set-2-1'], score['set-2-2']))
                add_events(last_event, events, 'set-3-start', frame_no)
            elif flags[FLAG_SET_3_SCORE]:
                if flags[FLAG_IS_WINNER_1]:
                    score['set-3-1'] += 1
                    add_events(last_event, events, 'set-3-winner-1', frame_no)
                else:
                    score['set-3-2'] += 1
                    add_events(last_event, events, 'set-3-winner-2', frame_no)
        else:
            continue
    return events


def show_events(events):
    for event_name, timestamp, content in events:
        print(event_name, timestamp, content)




def plot_flags(flags_seq):
    names = ['v2.2.4', 'v3.0.3', 'v3.0.2', 'v3.0.1', 'v3.0.0', 'v2.2.3',
             'v2.2.2', 'v2.2.1', 'v2.2.0', 'v2.1.2', 'v2.1.1', 'v2.1.0',
             'v2.0.2', 'v2.0.1', 'v2.0.0', 'v1.5.3', 'v1.5.2', 'v1.5.1',
             'v1.5.0', 'v1.4.3', 'v1.4.2', 'v1.4.1', 'v1.4.0']

    dates = ['2019-02-26', '2019-02-26', '2018-11-10', '2018-11-10',
             '2018-09-18', '2018-08-10', '2018-03-17', '2018-03-16',
             '2018-03-06', '2018-01-18', '2017-12-10', '2017-10-07',
             '2017-05-10', '2017-05-02', '2017-01-17', '2016-09-09',
             '2016-07-03', '2016-01-10', '2015-10-29', '2015-02-16',
             '2014-10-26', '2014-10-18', '2014-08-26']

    # Convert date strings (e.g. 2014-10-18) to datetime
    dates = [datetime.strptime(d, "%Y-%m-%d") for d in dates]
    levels = np.tile(
        [-5, 5, -3, 3, -1, 1],
        int(np.ceil(len(dates) / 6))
    )[:len(dates)]

    fig, ax = plt.subplots(figsize=(8.8, 4), constrained_layout=True)
    ax.set(title='Matplotlib rel. dates')

    ax.vlines(dates, 0, levels, color='tab:red')
    ax.plot(
        dates, np.zeros_like(dates), '-o', color='k', markerfacecolor='w'
    )

    for d, l, r in zip(dates, levels, names):
        ax.annotate(
            r, xy=(d, l), xytext=(-3, np.sign(l) * 3), textcoords='offset points',
            horizontalalignment='right',
            verticalalignment='bottom' if l > 0 else 'top'
        )

    ax.xaxis.set_major_locator(mticker.MaxNLocatior(5))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    plt.setp(ax.get_xticklabels(), rotation=30, ha='right')

    ax.yaxis.set_visible(False)
    ax.spines[['left', 'top', 'right']].set_visible(False)

    ax.margins(y=0.1)
    plt.show()


def main():
    videos = glob.glob('videos/videos/*.mp4')
    video_path = videos[0]
    print(video_path)
    capture_instance = cv2.VideoCapture(video_path)

    # capture_instance.set(cv2.CAP_PROP_POS_FRAMES, 795 * 50 + 10000)
    # _, frame = capture_instance.read()
    # cv2.imshow('frame', frame)
    # func_args = [
    #     (component_detection, (frame, 'match-bottom')),
    #     (set_detection, (frame, 'set-1')),
    #     (score_detection, (frame, 'set-1-score')),
    #     (set_detection, (frame, 'set-2')),
    #     (score_detection, (frame, 'set-2-score')),
    #     (set_detection, (frame, 'set-3')),
    #     (score_detection, (frame, 'set-3-score')),
    #     (winner_detection, (frame,)),
    # ]
    # flags = [func(*arg) for func, arg in func_args]
    # print(flags)
    # cv2.waitKey(0)
    # return
    flags_seq = process_video(capture_instance)

    plt.hist(TEMP['set-1-score'], bins=60)
    plt.show()

    events = catch_events(flags_seq)
    for event in events:
        print(event)
        capture_instance.set(cv2.CAP_PROP_POS_FRAMES, event[1] - SPEED)
        _, frame_a = capture_instance.read()
        capture_instance.set(cv2.CAP_PROP_POS_FRAMES, event[1] + 1)
        _, frame_b = capture_instance.read()
        cv2.imshow('frame', cv2.resize(np.hstack([frame_a, frame_b]), (0, 0), fx=0.7, fy=0.7))
        cv2.waitKey(0)


    # plot_flags(flags_seq)



if __name__ == '__main__':
    main()