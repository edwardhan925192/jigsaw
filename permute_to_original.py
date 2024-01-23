from PIL import Image
import matplotlib.pyplot as plt

def draw_rearranged_tiles(img_path, tile_order):
    # Load the image
    raw_img = Image.open(img_path)

    width, height = raw_img.size
    cell_width, cell_height = width // 4, height // 4

    tiles = []
    for row in range(4):
        for col in range(4):
            tile = raw_img.crop((col * cell_width, row * cell_height,
                                 (col + 1) * cell_width, (row + 1) * cell_height))
            tiles.append(tile)

    # Rearrange the tiles according to tile_order
    rearranged_tiles = [None] * 16
    for new_position, original_position in enumerate(tile_order):
        rearranged_tile = tiles[new_position]
        rearranged_tiles[original_position - 1] = rearranged_tile


    # Create a new image to place rearranged tiles
    rearranged_img = Image.new("RGB", (width, height))

    for i, tile in enumerate(rearranged_tiles):
        row, col = divmod(i, 4)  # Swap the order here for row-wise arrangement
        rearranged_img.paste(tile, (col * cell_width, row * cell_height))

    # -- for checking
    rearranged_img.show()

    return rearranged_img
