import cv2
import pygame
import numpy as np


def cvimage_to_pygame(image, upscale=1):
    """Convert cvimage into a pygame image"""

    im_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Rescale the image if upscale > 1
    if upscale > 1:
        im_rgb = cv2.resize(
            im_rgb,
            (image.shape[1] * upscale, image.shape[0] * upscale),
            interpolation=cv2.INTER_NEAREST,
        )

    # For some reason the axes are swapped for pygame
    im_rgb = np.swapaxes(im_rgb, 0, 1)

    return pygame.surfarray.make_surface(im_rgb)
