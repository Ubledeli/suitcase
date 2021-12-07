import cv2
import numpy as np
from scipy import ndimage


def overlay(image, wheel_img, brake_img, gas_img, angle=0, brake=False, gas=False):
    wheel = ndimage.rotate(wheel_img, angle, reshape=False)
    empty = np.zeros_like(image)
    empty[20:220, -220:-20, :] = wheel
    if brake:
        empty[240 + 30:240 + 128, 1220:1220 + 70, :] = brake_img
    if gas:
        empty[240 + 30:240 + 128, 1220 + 70:1220 + 128, :] = gas_img
    image = cv2.addWeighted(image, 0.5, empty, 1, 0)
    return image

