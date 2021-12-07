import numpy as np


def normalize_img(arr):
    max_val = np.max(arr)
    min_val = np.min(arr)
    arr = np.array(arr)
    return (arr - min_val) / (max_val - min_val + 1e-8)
