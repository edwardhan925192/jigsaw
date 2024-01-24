import cv2
import numpy as np
from matplotlib import pyplot as plt
from realesrgan import RealESRGAN

# -- increasing contrast
def increase_contrast(image_path):
    image = cv2.imread(image_path)
    image_yuv = cv2.cvtColor(image, cv2.COLOR_BGR2YUV)
    image_yuv[:,:,0] = cv2.equalizeHist(image_yuv[:,:,0])
    image_output = cv2.cvtColor(image_yuv, cv2.COLOR_YUV2BGR)
    return image_output


# -- color space
def convert_color_spaces(image_path):
    image = cv2.imread(image_path)
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    image_lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    return image_hsv, image_lab


def sharpen_image(image_path):
    image = cv2.imread(image_path)
    kernel_sharpening = np.array([[-1,-1,-1],
                                  [-1, 9,-1],
                                  [-1,-1,-1]])
    sharpened_image = cv2.filter2D(image, -1, kernel_sharpening)
    return sharpened_image


# -- histogram equalization
def histogram_equalization(image_path):
    image = cv2.imread(image_path, 0)
    equalized_image = cv2.equalizeHist(image)
    return equalized_image



# -- resolution
def non_upscaling_enhancement(image_path):
    enhancer = RealESRGAN(device='cuda')  # or use 'cpu'
    img = cv2.imread(image_path, cv2.IMREAD_UNCHANGED)
    enhanced_img = enhancer.enhance(img, outscale=1)
    return enhanced_img



# -- edge sharpening
def unsharp_mask(image, sigma=1.0, strength=1.5):
    blurred = cv2.GaussianBlur(image, (0, 0), sigma)
    sharpened = cv2.addWeighted(image, 1.0 + strength, blurred, -strength, 0)
    return sharpened


# ================================== MAIN FUNCTION ==================================  # 

import zipfile
import os
import cv2
from tqdm import tqdm

# -- configs
zip_file_path = '/content/drive/MyDrive/jigsaw puzzle/shuffled_ver1.zip'
extract_to_directory = '/content/pre_augmentation'
pre_augmentation = 'pre_augmentation'
post_augmentation = 'post_augmentation'
save_dir = '/content/post_augmentation'
zip_name = 'hsv_shuffled_ver1.zip'
# -- 

os.makedirs(extract_to_directory, exist_ok=True)

with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    zip_ref.extractall(extract_to_directory)

folder_path = f'/content/{pre_augmentation}'

image_paths = []

for filename in tqdm.tqdm(os.listdir(folder_path), desc="Collecting images"):
  if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tiff')):  # Check for image files
      image_path = os.path.join(folder_path, filename)
      files = (image_path, filename)
      image_paths.append(files)

# -- augmentation, changing name
for (img_path, img_name) in tqdm.tqdm(image_paths, desc="Processing images"):
  hsv,_ = convert_color_spaces(img_path)
  hsv = Image.fromarray(hsv)  
  hsv.save(f'/content/{post_augmentation}/hsv_{img_name}')  

# -- zip it 
zip_path = os.path.join(save_dir, zip_name)
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
    for root, _, files in os.walk(save_dir):
        for file in files:
            file_path = os.path.join(root, file)
            # Check to ensure the zip file is not including itself
            if file_path != zip_path:
                zipf.write(file_path, os.path.relpath(file_path, save_dir))
                os.remove(file_path)  # Delete the file after adding it to the zip

# -- move
import shutil
shutil.copy(f"{save_dir}/{zip_name}", "/content/drive/MyDrive/jigsaw puzzle/")
