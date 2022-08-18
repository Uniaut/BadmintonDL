import csv
import glob
import os

import numpy as np
import torch
import pandas as pd
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import (
    Compose,
    Normalize,
    RandomCrop,
    Resize,
    ToTensor,
)
from torchvision.transforms import functional as TF

import src.config as config


# Dataloader of labels:
class BadmintonDataset(Dataset):
    def __init__(self, data_path, transform=None):
        self.data_path = data_path
        self.transform = transform
        self.labels = self.load_labels()

    def load_labels(self):
        labels = []
        play_tuple = []
        with open(self.data_path, 'r', newline='\n') as tsvfile:
            readCSV = csv.reader(tsvfile, delimiter='\t')
            for row in readCSV:
                frame_no, desc = row
                frame_no = int(frame_no)
                if desc.startswith('play_start'):
                    start = frame_no
                if desc.startswith('score') and start is not None:
                    end = frame_no
                    play_tuple.append((start, end, desc))
                    start, end = None, None
        for play in play_tuple:
            labels.append((play[0], play[1], play[2]))
        return labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        label = self.labels[idx]
        image_path = label[0]
        image = Image.open(image_path)
        if self.transform:
            image = self.transform(image)
        return image, label[1]

if __name__ == '__main__':
    labels = glob.glob(os.path.join(config.LABELS_PATH, '*.tsv'))
    for label_path in labels:
        dl = BadmintonDataset(data_path=label_path)