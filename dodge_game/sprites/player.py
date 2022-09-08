# Define a Player object by extending pygame.sprite.Sprite

# The surface drawn on the screen is now an attribute of 'player'
import pygame
from pygame.constants import K_UP, K_DOWN, K_LEFT, K_RIGHT
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, SCREEN_WIDTH, SCREEN_HEIGHT):

        super(Player, self).__init__()

        self.SCREEN_WIDTH = SCREEN_WIDTH
        self.SCREEN_HEIGHT = SCREEN_HEIGHT

        self.width = 50
        self.height = 50

        self.surf = pygame.image.load(
            os.path.join(
                os.path.dirname(os.path.abspath(__file__)),
                "images",
                "Vantage-AI-square.png",
            )
        )

        self.surf = pygame.transform.scale(self.surf, (self.width, self.height))
        self.player_rect = self.surf.get_rect()

        # Put player at the center
        surf_center = (
            (self.SCREEN_WIDTH - self.surf.get_width()) / 2,
            (self.SCREEN_HEIGHT - self.surf.get_height()) / 2,
        )
        self.player_rect.move_ip(surf_center)

        self.rect = self.player_rect

        # Save the previous x and y locations
        self.prev_x = surf_center[0]
        self.prev_y = surf_center[1]

    # Move the sprite based on user keypresses

    # Updates using keypresses
    def update(self, user_x, user_y, pressed_keys, mouse_and_keyboard_controls):
        if mouse_and_keyboard_controls:
            # Use the mouse and keyboard as controlls
            # If the mouse is on screen, update using mouse
            if pygame.mouse.get_focused():
                # Let the player follow the mouse, otherwise teleporting is too easy
                x, y = pygame.mouse.get_pos()

                self.player_rect.centerx = x
                self.player_rect.centery = y

                # # Code to let the player follow the cursor:
                # dx = x - self.player_rect.centerx
                # dy = y - self.player_rect.centery
                # follow_speed = 0.2
                # self.player_rect.centerx = self.player_rect.centerx + follow_speed * dx
                # self.player_rect.centery = self.player_rect.centery + follow_speed * dy
            else:
                # Use the arrow keys
                if pressed_keys[K_UP]:
                    self.player_rect.move_ip(0, -5)

                if pressed_keys[K_DOWN]:
                    self.player_rect.move_ip(0, 5)

                if pressed_keys[K_LEFT]:
                    self.player_rect.move_ip(-5, 0)

                if pressed_keys[K_RIGHT]:
                    self.player_rect.move_ip(5, 0)
        else:
            # Use the given user_x and user_y as location
            self.player_rect.centerx = user_x
            self.player_rect.centery = user_y

        # Keep player on the screen

        if self.player_rect.left < 0:
            self.player_rect.left = 0

        if self.player_rect.right > self.SCREEN_WIDTH:
            self.player_rect.right = self.SCREEN_WIDTH

        if self.player_rect.top <= 0:
            self.player_rect.top = 0

        if self.player_rect.bottom >= self.SCREEN_HEIGHT:
            self.player_rect.bottom = self.SCREEN_HEIGHT

        # Create a rectangle between the current position and the previous position, this way a player cannot teleport through obstacles

        collision_rect = pygame.Rect(
            (
                min(self.player_rect.centerx, self.prev_x),
                min(self.player_rect.centery, self.prev_y),
            ),
            (
                max(self.player_rect.centerx, self.prev_x)
                - min(self.player_rect.centerx, self.prev_x),
                max(self.player_rect.centery, self.prev_y)
                - min(self.player_rect.centery, self.prev_y),
            ),
        )

        # Add the collistion rectangle to the player rectangle for collistion
        self.rect = self.player_rect.union(collision_rect)

        # Update the previous locations
        self.prev_x = self.player_rect.centerx
        self.prev_y = self.player_rect.centery

    def draw(self, screen):
        # Draw the player on the screen
        screen.blit(self.surf, self.player_rect)

        # Debug the collision rectangle
        # pygame.draw.rect(screen, (255,255,255), self.rect)
