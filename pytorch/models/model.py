import numpy as np
import torch
from torch import nn
import torch.nn.functional as F
from torch.nn import ReLU
from torchvision import models


class ResModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = models.resnet34(pretrained=True)

    def forward(self, inputs):
        out = self.features(inputs)
        return out
