import cv2
import numpy as np
import matplotlib.pyplot as plt
import numpy.ma as ma
import matplotlib.colors
import torch
import torch.nn.functional as F
# import kornia


def alter_water(img, label, label_index, color_hex='#9d2e93'):
    color = np.array(matplotlib.colors.to_rgb(color_hex))[::-1]*255
    water_mask = np.array(label == label_index, dtype=int)
    masked = ma.array(img, mask=1 - water_mask)
    mean = masked.mean(axis=(0, 1))
    water = water_mask * (img - mean + color)
    rest = img * (1 - water_mask)
    return water + rest


def alter_water_torch(img, label, label_index, color_hex='#9d2e93'):
    color = torch.tensor(matplotlib.colors.to_rgb(color_hex), device=img.device)[..., [2, 1, 0]] * 255  # RGB BGR
    water_mask = (label == label_index).float()
    masked = img * water_mask
    mean = masked[..., :].sum(dim=(0, 1)) / water_mask.sum()
    water = water_mask * (img - mean + color)
    rest = img * (1 - water_mask)
    return water + rest
