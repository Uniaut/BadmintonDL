import os


CHANNEL_URL = 'https://www.youtube.com/c/bwftv/videos'
PLAYLIST_URL = 'https://www.youtube.com/watch?v=teUN-6Us8Uw&list=PLA7ZcagI0frAvDm00pnfYC8hrSlfOXs_Z'

VIDEO_FPS = 30
VIDEOS_ROOT = os.path.join('R:', 'Datasets', 'BadmintonDL')
VIDEOS_PATH = os.path.join(VIDEOS_ROOT, 'videos')
VIDEOS_ARCHIVE_PATH = os.path.join(VIDEOS_ROOT, 'videos_list.txt')
MINIMUM_DURATION = 3 * 3600

CONDITION_IMAGE_FILE_PATH = os.path.join('src', 'etl', 'transform', 'feature_extract', 'images')


TESSERACT_PATH = os.path.join('C:', 'Program files', 'Tesseract-OCR', 'tesseract.exe')
TESSERACT_CONFIG = f'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'

IS_LOGO_THRESHOLD = 100.0
SCORE_AREA_VALIDITY_THRESHOLD = 1000.0

LABELS_PATH = os.path.join('labels')
