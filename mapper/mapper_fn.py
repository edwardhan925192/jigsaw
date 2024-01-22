import pandas as pd
from collections import Counter
from tqdm import tqdm

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


def map_and_assign_rowwise(df_A, df_B, mapper):
    # Iterate over each row
    for idx in tqdm(range(len(df_A)), desc="Processing Rows"):
        for key, indices in mapper.items():            
            values = df_A.iloc[idx, indices].values            
            most_common_value, _ = Counter(values).most_common(1)[0]            
            df_B.at[idx, key] = most_common_value


def mapper_main(preds):

    # -- finding max index 
    max_column_indices = preds.idxmax(axis=1) + 1
    chunk_size = 576
    reshaped_array = max_column_indices.values.reshape(-1, chunk_size)
    new_df = pd.DataFrame(reshaped_array)
    new_df.columns = range(1, chunk_size + 1)

    # -- dataframe b
    num_rows = 59961
    num_cols = 16

    column_names = [str(i) for i in range(1, num_cols + 1)]
    df = pd.DataFrame(0, index=range(num_rows), columns=column_names)

    # -- making mapper 
    mapper = create_mapping(True)
    map_576_to_16 = {}

    # Mapping 24 x 24 to 4 x 4
    for i in range(1, 17):
        map_576_to_16[i] = generate_sequence(mapper[i])

    map_and_assign_rowwise(new_df, df, mapper)

    return df 

