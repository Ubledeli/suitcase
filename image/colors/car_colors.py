import matplotlib
import cv2
import numpy as np
import matplotlib.pyplot as plt
from random import randint


def draw_histogram(image='test_images/zeleni.png'):
    bins = [0, 5, 25, 35, 55, 65, 85, 95, 115, 125, 145, 155, 175, 180]
    frame = cv2.imread(image)
    hls = cv2.cvtColor(frame, cv2.COLOR_BGR2HLS)
    # hls = hls[::2, ::2, :]  # halve linear dims
    hue_hist, edges = np.histogram(hls[:, :, 0].ravel(), bins=bins)
    saturation_hist, _ = np.histogram(hls[:, :, 2].ravel(), bins=100)
    lightness_hist, _ = np.histogram(hls[:, :, 1].ravel(), bins=100)
    hue_sum = np.sum(hue_hist)
    added_hist = saturation_hist + lightness_hist
    multiplied = saturation_hist * lightness_hist
    diff = lightness_hist - saturation_hist
    saturation_sum = np.sum(saturation_hist)
    saturation_start = np.sum(saturation_hist[0:20])
    lightness_end = np.sum(lightness_hist[10:90])
    lightness_sum = np.sum(lightness_hist)

    plt.plot(hue_hist * 0, label=f'hue: {hue_sum}')
    plt.plot(saturation_hist, label=f'saturation: {saturation_start / saturation_sum}')
    plt.plot(lightness_hist, label=f'lightness: {lightness_end / lightness_sum}')
    # plt.plot(added_hist, label=f'added: {np.sum(added_hist[0:30]) / np.sum(added_hist)}')
    plt.plot(added_hist, label=f'added: {np.sum(added_hist[0:30]) / np.sum(added_hist)}')
    # plt.plot(multiplied, label=f'multiplied: ')
    plt.legend()
    plt.show()


def car_color(crop, colors):
    bins = [0, 5, 25, 35, 55, 65, 85, 95, 115, 125, 145, 155, 175, 180]
    np_hist, edges = np.histogram(crop[:, :, 0].ravel(), bins=bins)
    saturation_hist, _ = np.histogram(crop[:, :, 2].ravel(), bins=100)
    lightness_hist, _ = np.histogram(crop[:, :, 1].ravel(), bins=100)
    added_hist = saturation_hist + lightness_hist
    np_hist[0] += np_hist[-1]
    np_hist = np_hist[0:-1:2]
    if np.sum(lightness_hist[-10:]) / np.sum(lightness_hist) > 0.2:  # white
        color = (255, 255, 255)
    elif np.sum(added_hist[0:30]) / np.sum(added_hist) > 0.7:  # black
        color = (0, 0, 0)
    elif np.sum(saturation_hist[0:20]) / np.sum(saturation_hist) > 0.7 and \
            np.sum(lightness_hist[10:90]) / np.sum(lightness_hist) > 0.7:
        color = (150, 150, 150)
    else:
        color = [int(x * 255) for x in matplotlib.colors.to_rgba(colors[np_hist.argmax()])[:-1]]
    return color
