import cv2
import pytesseract

tsrt_path = r'C:/Program Files/Tesseract-OCR/tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tsrt_path
tsrt_config = f'--oem 3 --psm 8 -c tessedit_char_whitelist=0123456789'


def text_from_img(image: cv2.Mat) -> str:
    if len(image.shape) == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
    text = pytesseract.image_to_string(image, config=tsrt_config)
    return text