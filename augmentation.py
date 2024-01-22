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
