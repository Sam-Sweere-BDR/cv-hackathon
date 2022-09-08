import os

import pygame

from dodge_game.utils import rhash, un_rhash

# Make it a sprite such that we can call it with the same functions
class LevelTimer(pygame.sprite.Sprite):
    def __init__(self, level_settings):
        super(LevelTimer, self).__init__()
        self.save_file_path = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "..", "save_file.txt"
        )

        self.level_settings = level_settings

        self.font = pygame.font.SysFont("Consolas", 30)

        self.start_ticks = pygame.time.get_ticks()  # starter tick

        self.level = self.read_savefile()

        self.seconds = 0

        self.start_seconds = self.level * self.level_settings["level_time"]

        self.level_time = level_settings["level_time"]  # Time of each level in seconds

        # Needed for sprite
        self.rect = None

        # Video fps
        self.v_fps = 0

    def reset(self):
        self.__init__(self.level_settings)

    def read_savefile(self):
        if os.path.exists(self.save_file_path):
            with open(self.save_file_path) as file:
                data = file.read()
                data = int(data)
                # unhash the number
                level = un_rhash(data)

                if level > 1000:
                    print("Nice try, but not today :)")
                    print("https://youtu.be/dQw4w9WgXcQ")
                    return 0

                return level
        else:
            return 0

    def write_savefile(self):
        # Remove the save file if it exists
        if os.path.exists(self.save_file_path):
            os.remove(self.save_file_path)

        # Hash the level to make it harder to cheat
        level_h = rhash(self.level)

        f = open(self.save_file_path, "a")
        f.write(str(level_h))
        f.close()

    def reset_savefile(self):
        # Remove the save file if it exists
        if os.path.exists(self.save_file_path):
            os.remove(self.save_file_path)

        self.reset()

    def update(self):
        self.seconds = (
            self.start_seconds + (pygame.time.get_ticks() - self.start_ticks) / 1000
        )  # calculate how many seconds

        # Increase the level every self.level_time
        if self.seconds > self.level_time * (self.level + 1):
            self.level += 1

    def draw(self, screen):
        screen.blit(
            self.font.render(f"Level: {self.level}", True, (255, 0, 0)), (15, 10)
        )
        screen.blit(
            self.font.render(str(round(self.seconds, 2)), True, (255, 0, 0)), (15, 40)
        )

        screen.blit(
            self.font.render(f"Video fps: {round(self.v_fps)}", True, (255, 0, 0)),
            (1030, 10),
        )

    def get_time(self):
        return self.seconds

    def get_level_settings(self):

        if self.level >= len(self.level_settings["levels"]):
            # We ran out of defined levels, cycle again through all the levels but increase the speed
            level_setting = self.level_settings["levels"][
                self.level % len(self.level_settings["levels"])
            ].copy()
            multiplier = int(self.level / len(self.level_settings["levels"]))
            level_setting["speed"] += multiplier * level_setting["speed"]

        else:
            level_setting = self.level_settings["levels"][self.level].copy()

        return level_setting
