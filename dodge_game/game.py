# PyGame template.
import os

# Import standard modules.
import sys

# Import non-standard modules.
import pygame
import pygame.camera
import yaml

from camera_controller import CameraController

# Define constants for the screen width and height
from dodge_game.camera.camera_controller_handler import CameraControllerHandler
from dodge_game.camera.utils import cvimage_to_pygame
from dodge_game.sprites.game_over_screen import GameOverScreen
from dodge_game.sprites.obstacle_handler import ObstacleHandler
from dodge_game.sprites.player import Player

from dodge_game.sprites.level_timer import LevelTimer

from pygame.locals import (
    K_KP_ENTER,
    K_RETURN,
    K_ESCAPE,
    KEYDOWN,
    K_r,
    QUIT,
)

CAMERA_WIDTH = 640
CAMERA_HEIGHT = 480
UPSCALE_FACTOR = 2
SCREEN_WIDTH = CAMERA_WIDTH * UPSCALE_FACTOR
SCREEN_HEIGHT = CAMERA_HEIGHT * UPSCALE_FACTOR


CAMERA_DEVICE = 0  # 0 for internal camera, 4 for external camera

# Hacky solution, last minute fix
CAMERA_DEVICE = CameraController().camera_id

MOUSE_AND_KEYBOARD_CONTROLS = False  # Set to True to enable mouse and keyboard controls


def quit_pygame():
    pygame.quit()
    sys.exit()


def update(
    dt, player, obstacle_handler, level_timer, camera_controller
):  # obstacles, all_sprites,
    """
    Update game. Called once per frame.
    dt is the amount of time passed since last frame.
    If you want to have constant apparent movement no matter your framerate,
    what you can do is something like

    x += v * dt

    and this will scale your velocity based on time. Extend as necessary."""

    # Go through events that are passed to the script by the window.
    for event in pygame.event.get():

        if event.type == QUIT:
            quit_pygame()

    # Get the set of keys pressed and check for user input
    pressed_keys = pygame.key.get_pressed()

    # Important, update the level timer first
    level_timer.update()

    # Update the player sprite based on user keypresses or camera_controller
    player.update(
        user_x=camera_controller.x * UPSCALE_FACTOR,
        user_y=camera_controller.y * UPSCALE_FACTOR,
        pressed_keys=pressed_keys,
        mouse_and_keyboard_controls=MOUSE_AND_KEYBOARD_CONTROLS,
    )

    obstacle_handler.update()

    # Check if any enemies have collided with the player
    if pygame.sprite.spritecollideany(player, obstacle_handler.obstacles):
        # If so, then remove the player and stop the loop

        return False

    return True


def draw(screen, all_sprites, camera_controller):
    """
    Draw things to the window. Called once per frame.
    """
    # screen.fill((0, 0, 0))  # Fill the screen with black.
    image = camera_controller.get_image()

    image = cvimage_to_pygame(image, upscale=UPSCALE_FACTOR)

    screen.blit(image, (0, 0))
    # screen =

    # Draw the obstacles on the screen
    for sprite in all_sprites:
        sprite.draw(screen)

    # Flip the display so that the things we drew actually show up.
    pygame.display.flip()


def game_loop(screen, fps, fpsClock, camera_controller, level_timer):
    # Instantiate player. Right now, this is just a rectangle.
    player = Player(SCREEN_WIDTH=SCREEN_WIDTH, SCREEN_HEIGHT=SCREEN_HEIGHT)

    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)

    # Add the level timer to all the sprites (for the draw)
    all_sprites.add(level_timer)

    # Create the obstacle handler
    obstacle_handler = ObstacleHandler(
        screen_width=SCREEN_WIDTH, screen_height=SCREEN_HEIGHT, level_timer=level_timer
    )
    all_sprites.add(obstacle_handler)

    alive = True

    # Main game loop.
    dt = 1 / fps  # dt is the time since last frame.

    while alive:  # Loop while alive
        if camera_controller.stopped is True:
            raise IOError("Camera controller stopped")

        alive = update(
            dt=dt,
            player=player,
            obstacle_handler=obstacle_handler,
            level_timer=level_timer,
            camera_controller=camera_controller,
        )  # You can update/draw here, I've just moved the code for neatness.

        draw(
            screen=screen, all_sprites=all_sprites, camera_controller=camera_controller
        )

        # Update the time
        dt = fpsClock.tick(fps)

    # Schow the game over screen (with the element in the background)
    time_score = level_timer.get_time()
    game_over_screen = GameOverScreen(time_score=time_score)
    all_sprites.add(game_over_screen)
    draw(screen=screen, all_sprites=all_sprites, camera_controller=camera_controller)

    # Write the save file and reset the level_timer`
    level_timer.write_savefile()
    level_timer.reset()

    # Return the time
    return level_timer.get_time()


def run_py_game():
    # Initialise PyGame.
    pygame.init()

    # Load the level config
    with open(os.path.join("dodge_game", "levels.yaml")) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        level_settings = yaml.load(file, Loader=yaml.FullLoader)

    # Create the timer
    level_timer = LevelTimer(level_settings=level_settings)

    # initializing and starting multi-threaded webcam input stream
    camera_controller_handler = CameraControllerHandler(
        webcam_stream_id=CAMERA_DEVICE,
        camera_width=CAMERA_WIDTH,
        camera_height=CAMERA_HEIGHT,
        level_timer=level_timer,
    )  # 0 id for main camera
    camera_controller_handler.start()  # processing frames in input stream

    # Set up the clock. This will tick every frame and thus maintain a relatively constant framerate. Hopefully.
    fps = 60.0
    fpsClock = pygame.time.Clock()

    # Set up the window.
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    running = True
    while running:
        # Run the game
        time_score = game_loop(
            screen, fps, fpsClock, camera_controller_handler, level_timer
        )

        # The player died
        wait_for_new_game = True

        pygame.event.clear()
        while wait_for_new_game:
            event = pygame.event.wait()
            if event.type == QUIT:
                quit_pygame()
            elif camera_controller_handler.stopped is True:
                raise IOError("Camera controller stopped")
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    quit_pygame()
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    wait_for_new_game = False
                    # Reset the level timer
                    level_timer.reset()
                elif event.key == K_r:
                    # Reset the savefile
                    level_timer.reset_savefile()
                    wait_for_new_game = False
