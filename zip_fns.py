import zipfile
import os
import cv2
from tqdm import tqdm

# ==================== UNZIPPING ========================= #
zip_file_path = '/content/drive/MyDrive/jigsaw puzzle/shuffled_ver2.zip'
extract_to_directory = '/content/pre_augmentation'
os.makedirs(extract_to_directory, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_directory)


# ==================== SAVING ========================= #
zip_path = os.path.join(save_dir, zip_name)
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(save_dir):
            for file in files:
                file_path = os.path.join(root, file)
                # Check to ensure the zip file is not including itself
                if file_path != zip_path:
                    zipf.write(file_path, os.path.relpath(file_path, save_dir))
                    os.remove(file_path)  # Delete the file after adding it to the zip


# ==================== MOVING ========================= #
import shutil
shutil.copy("/content/shuffled_ver3/shuffled_ver3.zip", "/content/drive/MyDrive/jigsaw puzzle/")
