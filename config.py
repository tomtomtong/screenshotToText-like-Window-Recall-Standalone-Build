import os

# Use the current working directory (the same folder as main.py)
base_folder = os.getcwd()

screenshots_path = os.path.join(base_folder, "screenshots")
texts_path = os.path.join(base_folder, "texts")

# Ensure the directories exist
os.makedirs(screenshots_path, exist_ok=True)
os.makedirs(texts_path, exist_ok=True)
