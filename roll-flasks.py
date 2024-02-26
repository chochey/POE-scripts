import pyautogui
import pytesseract
import cv2
import numpy as np
import time
import os
import keyboard
import re

# Explicitly set the path to the Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Set the TESSDATA_PREFIX environment variable to the directory containing the tessdata folder
os.environ["TESSDATA_PREFIX"] = r"C:\Program Files\Tesseract-OCR\tessdata"

# Create a directory to save the screenshots and preprocessed images
output_dir = r"C:\Users\Blue\Desktop\Repos\poetradechat\img"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

pyautogui.FAILSAFE = False


# Function to preprocess the image for text extraction
def preprocess_image(image):
    grayscale_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, thresholded_image = cv2.threshold(
        grayscale_image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )
    return thresholded_image


# Function to save preprocessed image
def save_preprocessed_image(image):
    timestamp = time.strftime("%Y%m%d%H%M%S")
    image_path = os.path.join(output_dir, f"preprocessed_image_{timestamp}.png")
    cv2.imwrite(image_path, image)


# Function to read and process screenshot using regular expressions
def read_and_process_screenshot(region, target_regex):
    screenshot = pyautogui.screenshot(region=region)
    screenshot_np = np.array(screenshot)
    screenshot_bgr = cv2.cvtColor(screenshot_np, cv2.COLOR_RGB2BGR)
    preprocessed_image = preprocess_image(screenshot_bgr)
    save_preprocessed_image(preprocessed_image)
    extracted_text = pytesseract.image_to_string(preprocessed_image, config="--psm 10")
    return extracted_text, all(regex.search(extracted_text) for regex in target_regex)


# Coordinates for the "trans" (x, y)
trans_position = (148, 360)
second_click_position = (2500, 1063)

# Region for reading the "burble" text (the bottom-right section of the screen)
burble_region = (
    pyautogui.size().width // 2,
    pyautogui.size().height // 2,
    pyautogui.size().width // 2,
    pyautogui.size().height // 2,
)

# Variable to track if Shift is held down
shift_held = False

# Define the list of target regular expressions
target_regex = [
    re.compile(r"\bGAIN 3 CHARGES WHEN YOU ARE HIT BY AN ENEMY\b", re.IGNORECASE),
    re.compile(r"\bINCREASED\s+EFFECT\b", re.IGNORECASE),
]

# Right-click once at the beginning
pyautogui.rightClick(trans_position)

# Hold Shift using pyautogui and left-click while checking for the "burble" text
stop_condition = False

for _ in target_regex:
    if stop_condition:
        break

    if not shift_held:
        pyautogui.keyDown("shift")  # Hold Shift
        shift_held = True
    pyautogui.click(second_click_position)

    # Wait for text to appear and check visibility (adjust delay as needed)
    time.sleep(1.5)  # Adjust delay if needed
    burble_text, match = read_and_process_screenshot(burble_region, target_regex)

    # Check if the regular expressions match the burble_text
    if match:
        stop_condition = True

# Release Shift key after the loop is finished
if shift_held:
    pyautogui.keyUp("shift")
