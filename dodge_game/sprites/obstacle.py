import pygame
import random


class Obstacle(pygame.sprite.Sprite):
    def __init__(
        self, screen_width, screen_height, width, height, x, y, direction, color
    ):

        super(Obstacle, self).__init__()
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.width = width
        self.height = height

        self.direction = direction

        self.surf = pygame.Surface((width, height))
        self.surf.fill(color)
        self.rect = self.surf.get_rect(x=x, y=y)

    def update(self):
        self.rect.move_ip(self.direction[0], self.direction[1])

        if (
            self.rect.right < 0
            or self.rect.left > self.screen_width
            or self.rect.bottom < 0
            or self.rect.top > self.screen_height
        ):
            self.kill()

    def draw(self, screen):
        screen.blit(self.surf, self.rect)


def create_obstacle(
    screen_width,
    screen_height,
    thickness,
    gap_size,
    direction,
    color=(255, 255, 255),
):

    # start_axis = None

    # Determine the start position
    if direction[0] != 0 and direction[1] != 0:
        # The object moves in both directions, choose a random start loc
        start_axis = random.choice(["hor", "vert"])
    elif direction[0] != 0:
        start_axis = "vert"
    elif direction[1] != 0:
        start_axis = "hor"
    else:
        raise ValueError("No moving direction indicated")

    gap_side_buffer = 5

    if start_axis == "hor":
        gap_location = random.randint(
            int(0.5 * gap_size + gap_side_buffer),
            int(screen_width - 0.5 * gap_size - gap_side_buffer),
        )
        left_width = gap_location - 0.5 * gap_size
        right_width = screen_width - gap_location - 0.5 * gap_size
        left_height = thickness
        right_height = thickness

        x_left = 0
        x_right = left_width + gap_size
        if direction[1] > 0:
            y_left = 0
            y_right = 0
        else:
            y_left = screen_height
            y_right = screen_height
    elif start_axis == "vert":
        gap_location = random.randint(
            int(0.5 * gap_size + gap_side_buffer),
            int(screen_height - 0.5 * gap_size - gap_side_buffer),
        )
        left_width = thickness
        right_width = thickness
        left_height = gap_location - 0.5 * gap_size
        right_height = screen_height - gap_location - 0.5 * gap_size

        y_left = 0
        y_right = left_height + gap_size
        if direction[0] > 0:
            x_left = 0
            x_right = 0
        else:
            x_left = screen_width
            x_right = screen_width

    else:
        raise ValueError(f"Axis {start_axis} unkown")

    left_obstacle = Obstacle(
        screen_width=screen_width,
        screen_height=screen_height,
        width=left_width,
        height=left_height,
        x=x_left,
        y=y_left,
        direction=direction,
        color=color,
    )
    right_obstacle = Obstacle(
        screen_width=screen_width,
        screen_height=screen_height,
        width=right_width,
        height=right_height,
        x=x_right,
        y=y_right,
        direction=direction,
        color=color,
    )

    return left_obstacle, right_obstacle
