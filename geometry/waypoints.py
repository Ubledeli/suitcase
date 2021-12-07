import numpy as np
import pygame
from pygame import gfxdraw
import torch
from geometry.trigonometry import orientation_angle, rotate_origin


def label(waypoints, name='points.png', number_of_waypoints=20, rotate=True, size=72, spacing=1.0):
    x_offset = size // 2
    y_offset = size - 1
    waypoints = waypoints.transpose().reshape(-1, 2) * spacing  # space out waypoints
    if rotate:
        angle = orientation_angle(waypoints)
        waypoints = rotate_origin(waypoints, angle-np.pi/2)
    latitudes = waypoints[:number_of_waypoints, 0] - waypoints[0, 0]
    longitudes = waypoints[:number_of_waypoints, 1] - waypoints[0, 1]
    surf = pygame.Surface((size, size))
    surf.fill((0, 0, 0))
    for lat, long in zip(latitudes, longitudes):
        # pygame.draw.circle(surf, (255, 255, 255), (size / 2 + lat, size / 2 + long), size / 32)
        gfxdraw.pixel(surf, int(x_offset - lat), int(y_offset - long), (255, 255, 255))
    pygame.image.save(surf, name)
    return latitudes, longitudes


def compass(waypoints, frame, name='points.png'):
    latitudes, longitudes = waypoints
    surface_size = 96
    try:
        lat = latitudes[frame + 1] - latitudes[frame]
        long = longitudes[frame + 1] - longitudes[frame]
    except:
        lat, long = 0, 0
    surf = pygame.Surface((surface_size, surface_size))
    surf.fill((0, 0, 0))
    center = (surface_size / 2, surface_size / 2)
    pygame.draw.line(surf, (255, 255, 255), center, (lat * 10, long * 10), width=surface_size // 20)
    pygame.image.save(surf, name)


def image_to_waypoints(img):
    waypoints = (img.mean(dim=0) > 0.5).float()
    waypoints = waypoints.nonzero()
    waypoints = torch.tensor([35.5, 71], device=img.device) - waypoints.flip(dims=(0, 1))
    # waypoints = waypoints[::2, :]  # every other point
    waypoints = waypoints.permute(1, 0)
    return waypoints

