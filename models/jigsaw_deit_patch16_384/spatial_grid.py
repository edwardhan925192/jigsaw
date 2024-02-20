import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms
from torchvision.io import read_image

import timm
from timm.data import create_transform
from timm.data.constants import IMAGENET_DEFAULT_MEAN, IMAGENET_DEFAULT_STD

import pandas as pd
import numpy as np
from PIL import Image
from tqdm.auto import tqdm

import os
import time

device = 'cuda' if torch.cuda.is_available() else 'cpu'

class Model(nn.Module):
    def __init__(self, pretrained = True):
        super().__init__()
        self.pretrained = pretrained

        deit3 = timm.create_model('deit3_base_patch16_384', pretrained = pretrained)

        self.patch_embed = deit3.patch_embed
        self.cls_token = deit3.cls_token
        self.blocks = deit3.blocks
        self.norm = deit3.norm

        self.adaptive_pool = nn.AdaptiveAvgPool2d((4, 4))

        self.jigsaw = nn.Sequential(
            nn.Linear(768, 768),
            nn.ReLU(),
            nn.Linear(768, 768),
            nn.ReLU(),
            nn.Linear(768, 4 * 4)
        )

    def forward(self, x):
        x = self.patch_embed(x)

        cls_tokens = self.cls_token.expand(x.shape[0], -1, -1)
        x = torch.cat((cls_tokens, x), dim=1)

        x = self.blocks(x)
        x = self.norm(x)

        x = x[:, 1:]  # Discard cls token
        x = x.reshape(x.shape[0], 24, 24, -1)  # Reshape to (batch_size, 24, 24, token_size)

        # Apply adaptive pooling
        x = self.adaptive_pool(x.permute(0, 3, 1, 2))
        x = x.permute(0, 2, 3, 1)  # Shape: (batch_size, 4, 4, 768)
        x = x.reshape(-1, 768)  # Flatten to process each patch: (batch_size * 4 * 4, 768)
        x = self.jigsaw(x)

        x = F.softmax(x, dim=-1)


        return x
