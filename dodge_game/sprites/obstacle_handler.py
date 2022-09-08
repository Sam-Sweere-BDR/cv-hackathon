import random

import pygame

from dodge_game.sprites.obstacle import create_obstacle


class ObstacleHandler(pygame.sprite.Sprite):
    def __init__(self, screen_width, screen_height, level_timer):
        super(ObstacleHandler, self).__init__()

        self.screen_width = screen_width
        self.screen_height = screen_height
        self.level_timer = level_timer

        # Needed for sprite
        self.rect = None

        # Set up list of obstacles that need to be updated every frame
        self.obstacles = pygame.sprite.Group()

    def create_obstacle(self):
        # Create the new enemy and add it to sprite groups
        # Direction is indicated in speed
        direction = random.choice([(1, 0), (-1, 0), (0, 1), (0, -1)])

        level_settings = self.level_timer.get_level_settings()

        speed = level_settings["speed"]  # + level_timer.get_time() / 10
        gap_size = level_settings["gap_size"]

        direction = (direction[0] * speed, direction[1] * speed)

        left_obstacle, right_obstacle = create_obstacle(
            screen_width=self.screen_width,
            screen_height=self.screen_height,
            thickness=25,
            gap_size=gap_size,
            direction=direction,
            color=(255, 255, 255),
        )

        self.obstacles.add(left_obstacle)
        self.obstacles.add(right_obstacle)

    def update(self):
        self.obstacles.update()

        # If there are no more obstacles create an obstacle
        if len(self.obstacles) == 0:
            self.create_obstacle()

    def draw(self, screen):
        for obstacle in self.obstacles:
            obstacle.draw(screen)
