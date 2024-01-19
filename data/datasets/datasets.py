import pandas as pd
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from PIL import Image
import torch

class DataFrameDataset_custom(Dataset):
    def __init__(self, dataframe, image_column, target_columns, transform=None):
        '''
        suppose image path and targets are all given in dataframe
        '''
        self.dataframe = dataframe
        self.image_column = image_column
        self.target_columns = target_columns
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):

        # -- df img path
        image_path = self.dataframe.iloc[idx][self.image_column]

        # -- modifying
        stripped_path = image_path[1:] if image_path.startswith('.') else image_path
        image_path = '/content' + stripped_path
        # --

        # -- image process
        # tensor_img = process_image(image_path)

        image = Image.open(image_path).convert('RGB')  # Convert to RGB for consistency

        if self.transform:
            image = self.transform(image)

        # -- targets
        targets = self.dataframe.iloc[idx][self.target_columns]
        targets = targets.astype(float)
        targets = torch.tensor(targets, dtype=torch.float32) - 1

        return image, targets

class DataFrameDataset_custom_test(Dataset):
    def __init__(self, dataframe, image_column, transform=None):
        '''
        suppose image path and targets are all given in dataframe
        '''
        self.dataframe = dataframe
        self.image_column = image_column
        self.transform = transform

    def __len__(self):
        return len(self.dataframe)

    def __getitem__(self, idx):

        # -- df img path
        image_path = self.dataframe.iloc[idx][self.image_column]

        # -- modifying
        stripped_path = image_path[1:] if image_path.startswith('.') else image_path
        image_path = '/content' + stripped_path

        image = Image.open(image_path).convert('RGB')  # Convert to RGB for consistency

        # -- image process
        #tensor_img = process_image(image_path)

        if self.transform:
            image = self.transform(image)

        return image

def dataset_prep(train_df, val_df, collater, batch_sizes, shuffle, transform ):
    # -- target col
    def generate_target_columns(start, end):
      return [str(i) for i in range(start, end + 1)]
    target_columns = generate_target_columns(1, 16)

    # -- train
    train_dataset = DataFrameDataset_custom(train_df, 'img_path', target_columns, transform=transform)
    if collater:
        train_dataloader = DataLoader(train_dataset, batch_size=batch_sizes, shuffle=shuffle, collate_fn=collater)
    else:
        train_dataloader = DataLoader(train_dataset, batch_size=batch_sizes, shuffle=shuffle)

    # -- validation
    val_dataset = DataFrameDataset_custom(val_df, 'img_path', target_columns, transform=transform)
    if collater:
        val_dataloader = DataLoader(val_dataset, batch_size=batch_sizes, shuffle=shuffle, collate_fn=collater)
    else:
        val_dataloader = DataLoader(val_dataset, batch_size=batch_sizes, shuffle=shuffle)

    return train_dataloader, val_dataloader
