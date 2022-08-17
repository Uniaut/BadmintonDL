import glob
import os

import cv2

import src.etl.transform.feature_extract.feature_extract as fe
import src.utils as utils

# detect of change on features of frame
def only_features(features: tuple) -> tuple:
    '''
    extract only features from with extra data
    PARAMETER:
        features: tuple - features
    RETURN:
        tuple - features
    '''
    return [feature for feature, extra in features]


def change_detection(sequence: list) -> list:
    '''
    detect of change on features of frame
    PARAMETER:
        sequence: list - sequence of features
    RETURN:
        list - sequence of events
    '''
    events = []
    for idx, element in enumerate(sequence):
        if idx == 0:
            continue

        frame_no, features = element
        prev_features = sequence[idx - 1][1]
        if only_features(features)[:2] != only_features(prev_features)[:2]:
            events.append((frame_no, prev_features, features))
    return events


def event_detection(sequence: list) -> list:
    '''
    detect of change on features of frame
    PARAMETER:
        sequence: list - sequence of features
    RETURN:
        list - sequence of events
    '''
    changes = change_detection(sequence)
    events = []
    for frame_no, prev_features, now_features in changes:
        now_features, prev_features = only_features(now_features), only_features(prev_features)
        now_logo, now_game, now_winner = now_features
        prev_logo, prev_game, _ = prev_features

        valid_event = False
        if now_logo and not prev_logo:
            events.append((frame_no, f'game start {now_game[0]}'))
            valid_event = True
        elif prev_logo and not now_logo:
            events.append((frame_no, f'game end {prev_game[0]}'))
            valid_event = True

        if prev_game[1] + 1 == now_game[1] or prev_game[2] + 1 == now_game[2]:
            court_swap = now_game[0] == 2 or (now_game[0] == 3 and (now_game[1] >= 11 or now_game[2] >= 11))
            winner_position = 'top' if court_swap ^ now_winner==1 else 'bottom'
            events.append((frame_no, f'score player {now_winner} on winner_position'))
            valid_event = True
        
        if not valid_event:
            events.append((frame_no, f'etc'))

    # insert play start event of every score event
    events_with_play_start = []
    for idx, event in enumerate(events):
        frame_no, event_tag = event
        
        if event_tag.startswith('score'):
            prev_frame_no, prev_event_tag = events[idx - 1]
            if prev_event_tag.startswith('score'):
                events_with_play_start.append((prev_frame_no + 200, 'play start'))
            elif prev_event_tag.startswith('game start'):
                events_with_play_start.append((prev_frame_no, 'play start'))
            
        events_with_play_start.append(event)

    return events_with_play_start



# simple heuristic validation code
if __name__ == '__main__':
    # get point score from frames in dummy directory
    frames = glob.glob(os.path.join('dummy', '*.png'))
    for frame_path in frames:
        frame = cv2.imread(frame_path)
        features = (
            fe.is_logo_on(frame),
            fe.get_score_data(frame),
        )
        print(only_features(features))
        cv2.imshow('frame', frame)
        cv2.waitKey(0)