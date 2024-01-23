import random
import numpy as np 

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
