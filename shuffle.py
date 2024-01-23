import random
import numpy as np 
import cv2
import os 

def shuffle_image(image):
        c, h, w = image.shape
        block_h, block_w = h//4, w//4
        shuffle_order = list(range(0, 16))
        random.shuffle(shuffle_order)
        image_shuffle = [[0 for _ in range(4)] for _ in range(4)]
        for idx, order in enumerate(shuffle_order):
            h_idx, w_idx = divmod(order,4)
            h_idx_shuffle, w_idx_shuffle = divmod(idx, 4)
            image_shuffle[h_idx_shuffle][w_idx_shuffle] = image[:, block_h * h_idx : block_h * (h_idx+1), block_w * w_idx : block_w * (w_idx+1)]
        image_shuffle = np.concatenate([np.concatenate(image_row, -1) for image_row in image_shuffle], -2)
        return image_shuffle, shuffle_order


def shuffle_and_save_images(source_folder, save_dir, custom_word):
    for filename in os.listdir(source_folder):
        # Check if the file is an image
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            image_path = os.path.join(source_folder, filename)

    # -- all I need 
    img = cv2.imread(image_path)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB if needed

    # Ensure the image is in C, H, W format
    img = img.transpose(2, 0, 1)  # OpenCV uses H, W, C format

    # -- 3. shuffle, get order
    img_shuffle, _ = shuffle_image(img)

    # -- 4. stack shuffled data such that it has data frame in the similar way of training
    base_filename = os.path.basename(image_path)

    shuffled_filename = f'{custom_word}_{base_filename}'
    save_path = os.path.join(save_dir, shuffled_filename)

    cv2.imwrite(save_path, img_shuffle.transpose(1, 2, 0))  # Convert back to H, W, C for saving
