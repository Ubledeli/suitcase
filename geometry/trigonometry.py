import numpy as np


def rotate_origin(xy, radians):
    x, y = xy[:, 0], xy[:, 1]
    xx = x * np.cos(radians) + y * np.sin(radians)
    yy = -x * np.sin(radians) + y * np.cos(radians)
    return np.array([xx, yy]).transpose()


def orientation_angle(waypoints):
    try:
        vector = waypoints[1] - waypoints[0]
        angle = np.arctan2(vector[1], vector[0])
    except IndexError:
        angle = 0
    return angle

