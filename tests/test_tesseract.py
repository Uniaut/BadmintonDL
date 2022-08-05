import numpy as np

import cv2
import pytesseract
tsrt_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tsrt_path
img_path = r'./tests/tesseract/test.jpg'
img_cv = cv2.imread(img_path)

# erode image
img_cv = cv2.resize(img_cv, (0, 0), fx=5.0, fy=5.0)
img_cv = cv2.erode(img_cv, None, iterations=2)
cv2.imshow('erode', img_cv)
img_cv = cv2.resize(img_cv, (0, 0), fx=0.2, fy=0.2)
cv2.waitKey(0)
# By default OpenCV stores images in BGR format and since pytesseract assumes RGB format,
# we need to convert from BGR to RGB format/mode:
img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
print((pytesseract.image_to_string(img_rgb, config=f'--oem {3} --psm {8} -c tessedit_char_whitelist=0123456789'),))