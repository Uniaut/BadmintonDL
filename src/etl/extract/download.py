import os

from yt_dlp import YoutubeDL

import src.config as config


def video_filter(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration < config.MINIMUM_DURATION:
        return 'The video is too short'


def filter_dl(urls, n):
    print(config.VIDEOS_PATH)
    ydl_opts = {
        'match_filter': video_filter,
        'outtmpl': '%(id)s.%(ext)s',
        'paths': {
            'home': config.VIDEOS_PATH,
            'temp': ''
        },
        'playlist_items': f':{n}',
        'ignoreerrors': True,
        'download_archive': config.VIDEOS_ARCHIVE_PATH,
    }
    with YoutubeDL(ydl_opts) as ydl_instance:
        error_code = ydl_instance.download(urls)
