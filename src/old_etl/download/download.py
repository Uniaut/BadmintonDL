import os

from yt_dlp import YoutubeDL

VIDEOS_PATH = os.path.join('videos', 'videos')
VIDEOS_ARCHIVE_PATH = os.path.join('videos', 'list.txt')


# ASSUME: cctv video is longer than 3 hours
def video_filter(info, *, incomplete):
    duration = info.get('duration')
    if duration and duration < 3 * 3600:
        return 'The video is too short'


def filter_dl(urls, n):
    ydl_opts = {
        'match_filter': video_filter,
        'outtmpl': '%(id)s.%(ext)s',
        'paths': {
            'home': VIDEOS_PATH,
            'temp': ''
        },
        'playlist_items': f':{n}',
        'ignoreerrors': True,
        'download_archive': VIDEOS_ARCHIVE_PATH,
    }
    with YoutubeDL(ydl_opts) as ydl_instance:
        error_code = ydl_instance.download(urls)
