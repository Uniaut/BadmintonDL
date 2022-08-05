import os
import numpy as np
import csv

import cv2
import tqdm

import src.config as config


def save_events_as_tsv(events: list[tuple[int, str]], video_id: str):
    '''
    save events to tsv file.
    PARAMETER:
        events: list[tuple[int, str]] - events to save
        video_id: str - video id
    '''
    file_path = os.path.join(config.LABELS_PATH, f'events_{video_id}.tsv')
    with open(file_path, 'w') as f:
        writer = csv.writer(f, delimiter='\t')
        writer.writerow(['frame_no', 'event'])
        for event in events:
            writer.writerow(event)
