def generate_sequence(start_number):
    sequence = []
    for i in range(6):  # Repeat for 6 rows
        # Add numbers 1 to 5 to the start number for each row
        sequence.extend([start_number + j for j in range(6)])
        # Move to the start of the next row, which is 24 places ahead
        start_number += 24
    return sequence

def create_mapping(base1 = False):
    # Given sequence
    if base1:
      sequence = [1, 7, 13, 19, 145, 151, 157, 163, 289, 295, 301, 307, 433, 439, 445, 451]
    else:
      sequence = [0, 6, 12, 18, 144, 150, 156, 162, 288, 294, 300, 306, 432, 438, 444, 450]

    # Create a mapping from 1-16 to the numbers in the sequence
    mapping = {i+1: sequence[i] for i in range(len(sequence))}

    return mapping

def convert_4x4_to_24x24_list(permutation_4x4):
    grid_24x24 = [0] * (24 * 24)
    block_size = 6
    for i in range(4):
        for j in range(4):
            value = permutation_4x4[i * 4 + j]
            start_index = (i * block_size * 24) + (j * block_size)
            for bi in range(block_size):
                for bj in range(block_size):
                    index = start_index + (bi * 24) + bj
                    grid_24x24[index] = value

    return grid_24x24

# ================ saving numbers in grid form ================= #

class GridManager:
    def __init__(self, grid_size=24, block_size=6):
        self.grid_size = grid_size
        self.block_size = block_size
        self.grid = np.zeros((grid_size, grid_size))

    def save_to_block(self, input_list, row_idx, col_idx):
        if len(input_list) != self.block_size ** 2:
            raise ValueError(f"Input list must have exactly {self.block_size ** 2} elements.")
        if not (0 <= row_idx < self.grid_size // self.block_size and 0 <= col_idx < self.grid_size // self.block_size):
            raise ValueError(f"Row and column indices must be in the range 0-{self.grid_size // self.block_size - 1}.")

        start_row = row_idx * self.block_size
        start_col = col_idx * self.block_size

        idx = 0
        for i in range(self.block_size):
            for j in range(self.block_size):
                self.grid[start_row + i][start_col + j] = input_list[idx]
                idx += 1

    def get_grid(self):
        return self.grid

    def reset(self):
        self.grid = np.zeros((self.grid_size, self.grid_size))

    def get_list(self):
        grid_list = []
        for row in range(self.grid_size):
            for col in range(self.grid_size):
                grid_list.append(self.grid[row][col])
        return grid_list

def map_to_576(target_lists, mapper, grid_manager):
  grid_manager.reset()

  # -- saving in the grid form
  for idx,target in enumerate(target_lists):

    # -- saving in the grid form
    sequence = generate_sequence(mapper[target])
    col_idx = idx % 4
    row_idx = idx // 4
    grid_manager.save_to_block(sequence, row_idx, col_idx)

  # -- return target of 24 x 24 in the list form.
  grid_as_list = grid_manager.get_list()
  return grid_as_list

