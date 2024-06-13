import os
import sys
import time
import traceback
from datetime import datetime

import mss
import numpy as np
from PIL import Image

import pytesseract
from config import screenshots_path, texts_path
from ocr import extract_text_from_image
from utils import timestamp_to_human_readable

def log_error(e):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("error_log.txt", "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] Exception occurred:\n{str(e)}\n\nTraceback:\n{traceback.format_exc()}\n\n")

def configure_tesseract_path():
    if hasattr(sys, '_MEIPASS'):
        tesseract_path = os.path.join(sys._MEIPASS, 'tesseract', 'tesseract.exe')
        tessdata_prefix = os.path.join(sys._MEIPASS, 'tessdata')
    else:
        tesseract_path = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
        tessdata_prefix = r'C:\Program Files\Tesseract-OCR\tessdata'
    
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    os.environ['TESSDATA_PREFIX'] = tessdata_prefix

configure_tesseract_path()

# Print the directories where files will be saved
print(f"Text files will be saved in: {texts_path}")
print(f"Screenshots will be saved in: {screenshots_path}")

# Ensure the directories exist
os.makedirs(screenshots_path, exist_ok=True)
os.makedirs(texts_path, exist_ok=True)

def take_screenshot():
    with mss.mss() as sct:
        monitor = sct.monitors[1]
        screenshot = np.array(sct.grab(monitor))[:, :, :3]  # Grab RGB only
        return screenshot

def resize_image(image, scale_factor):
    width, height = image.size
    new_size = (int(width * scale_factor), int(height * scale_factor))
    return image.resize(new_size, resample=Image.BICUBIC)

def save_screenshot(image, timestamp, quality=85, scale_factor=0.5):
    try:
        human_readable_timestamp = timestamp_to_human_readable(timestamp)
        filename = os.path.join(screenshots_path, f"{human_readable_timestamp}.jpg")
        resized_image = resize_image(image, scale_factor)
        resized_image.save(filename, format="JPEG", quality=quality)
    except Exception as e:
        log_error(e)

def save_text(text, timestamp):
    try:
        human_readable_timestamp = timestamp_to_human_readable(timestamp)
        filename = os.path.join(texts_path, f"{human_readable_timestamp}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"Timestamp: {human_readable_timestamp}\n\n{text}")
    except Exception as e:
        log_error(e)

def main():
    while True:
        try:
            screenshot = take_screenshot()
            image = Image.fromarray(screenshot)
            timestamp = time.time()
            save_screenshot(image, timestamp, quality=85, scale_factor=0.5)
            text = extract_text_from_image(image)
            save_text(text, timestamp)
            time.sleep(3)  # capture a screenshot every 3 seconds
        except Exception as e:
            log_error(e)
            time.sleep(60)  # Wait for 1 minute before trying again

if __name__ == "__main__":
    main()