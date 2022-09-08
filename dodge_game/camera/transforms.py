import time

import cv2
import numpy as np
import pygame


# def median_blu(x)


def brighten(x):

    x = x // 2 + 128

    return x


def darken(x):
    x = x // 10

    return x


def compress(x):
    x = x // 25

    x = x * 25

    return x

    # x = np.clip(0, amount, 255 - amount)
    #
    # x += np.ones_like(x)*amount

    # return x.astype(np.uint8)
    #
    # x = x/255
    #
    # x = np.sqrt(x)
    #
    # x = x*255
    #
    # return x.astype(np.uint8)


def add_gaussian_noise(x, amount):
    # x = x.astype(np.float16)
    x = np.clip(x, amount, 255 - amount) + np.random.uniform(
        0, amount, size=x.shape
    ).astype(np.uint8)
    # x = x/2
    # return np.clip(x, 0, 255).astype(np.uint8)

    return x


def disco(x):

    t = time.time()

    t = t * 10

    x[:, :, 0] += int(t)

    x[:, :, 1] += int(t * np.pi)

    x[:, :, 2] += int(t * np.e)
    return x


def hsv_disco(x, speed=1):
    x = cv2.cvtColor(x, cv2.COLOR_BGR2HSV)

    t = time.time()

    t = t * 10 * speed

    x[:, :, 0] += int(t)

    x[:, :, 1] += int(t * np.pi)

    x[:, :, 2] += int(t * np.e)

    x = cv2.cvtColor(x, cv2.COLOR_HSV2BGR)
    return x


def distort_image(image, transforms):
    function_config = {
        "Grayscale": lambda x: cv2.cvtColor(image, cv2.COLOR_BGR2GRAY),
        "Sobel": lambda x: cv2.Sobel(image, ddepth=cv2.CV_8UC1, dx=1, dy=1, ksize=5),
        "Normalize": lambda x: cv2.normalize(
            image, np.zeros_like(image), 0, 255, cv2.NORM_MINMAX
        ),  # (x - x.min()) / (x - x.min()).max() * 255,
        "Invert": lambda x: cv2.bitwise_not(image),  # x.max() - x,
        "Noise Low": lambda x: add_gaussian_noise(x, amount=40),
        "Noise High": lambda x: add_gaussian_noise(x, amount=100),
        "Median Blur": lambda x: cv2.medianBlur(x, 9),
        "Brighten": lambda x: brighten(x),
        "Darken": lambda x: darken(x),
        "Compress": lambda x: compress(x),
        "Disco": lambda x: disco(x),
        "HSV Disco": lambda x: hsv_disco(x),
        "HSV Rave": lambda x: hsv_disco(x, speed=50),
        "Erode": lambda x: cv2.erode(x, np.ones((15, 15), np.uint8), iterations=3),
        "Dilate": lambda x: cv2.dilate(x, np.ones((15, 15), np.uint8), iterations=3),
    }

    # level_config = {
    #     0: {},
    #     1: {"Grayscale"},
    #     2: {"Normalize", "Grayscale", "Sobel"},
    #     3: {"Normalize"},
    #     4: {"Invert"},
    # }

    for distortion_name in transforms:
        if distortion_name is None:
            continue
        distortion = function_config[distortion_name]
        image = distortion(image)

    # Make sure the image is always 3 layers
    if len(image.shape) != 3:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

    return image
