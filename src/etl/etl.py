import glob
import os

import cv2

import src.etl.extract.download as dl
import src.etl.transform.transform as tr
import src.etl.load.load as ld
import src.config as config


def main():
    # extract
    url = config.CHANNEL_URL
    dl.filter_dl(url, 70)

    # glob videos
    videos = glob.glob(os.path.join(config.VIDEOS_PATH, '*.mp4'))
    print('videos to process:')
    for video_path in videos:
        print(video_path)
    
    # transform & load
    for video_path in videos:
        print(video_path)
        video_id, _ = os.path.splitext(os.path.basename(video_path))
        # filter videos which is already labeled
        if os.path.exists(os.path.join(config.LABELS_PATH, f'{video_id}.txt')):
            print(f'{video_id} is already labeled')
            continue

        # transform video into events
        capture_instance = cv2.VideoCapture(video_path)
        events = tr.annotate_video(capture_instance)
        # load labels
        ld.save_events_as_tsv(events, video_id)




if __name__ == '__main__':
    main()