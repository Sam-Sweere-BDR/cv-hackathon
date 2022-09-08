import pygame

# Make it a sprite such that we can render it as the last frame with all the background elements still present
class GameOverScreen(pygame.sprite.Sprite):
    def __init__(self, time_score):
        super(GameOverScreen, self).__init__()
        self.font_size = 30
        font = pygame.font.SysFont("Consolas", 30)
        self.font_color = (0, 255, 0)
        self.text_location = (200, 100)

        text = [
            f"U Dead!",
            f"Time score: {time_score} seconds",
            "Press Enter to restart this level, Esc to quit",
            "Press 'R' to reset and start at level 0",
        ]
        self.label = []
        for line in text:
            self.label.append(font.render(line, True, self.font_color))

        self.rect = None

        print("U dead")
        print("Time score:", time_score)

    def update(self):
        pass

    def draw(self, screen):
        # screen.blit(self.font.render(self.text, True, self.font_color), self.text_location)

        for line_num in range(len(self.label)):
            screen.blit(
                self.label[line_num],
                (
                    self.text_location[0],
                    self.text_location[1]
                    + (line_num * self.font_size)
                    + (15 * line_num),
                ),
            )
