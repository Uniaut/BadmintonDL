from yt_dlp import YoutubeDL

from src.etl.extract import download


CHANNEL_URL = 'https://www.youtube.com/c/bwftv/videos'
PLAYLIST_URL = 'https://www.youtube.com/watch?v=teUN-6Us8Uw&list=PLA7ZcagI0frAvDm00pnfYC8hrSlfOXs_Z'

def main():
    ydl = YoutubeDL()
    url = CHANNEL_URL
    download.filter_dl(url, 5)


if __name__ == '__main__':
    main()