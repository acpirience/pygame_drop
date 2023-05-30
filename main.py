"""
        Drop7 project
"""
import os
import sys
import time
from collections import deque

import pygame
from loguru import logger

from states.menus.title import Title
from utils import draw_text

GAME_NAME = "Drop7 clone"
GAME_W = 1280
GAME_H = 720
SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720


class Game:  # pylint: disable=R0902
    """Main class where the game loop runs"""

    def __init__(self):
        logger.info("Starting")

        self.init_window()
        self.screen_width, self.screen_height, self.blit_w, self.blit_h = 0, 0, 0, 0
        self.blit_origin = (0, 0)
        self.previous_game_canvas = None
        self.screen = None
        self.init_screen()

        # Game statuses
        self.running = True
        self.started = False
        self.exit_requested = False
        self.paused = False

        # states
        self.state = None
        self.states = {}
        logger.info(f"Current state: {self.state}")
        logger.info(f"State list: {self.states}")
        self.load_states("Title")

        # timing
        self.delta_time = 0.0
        self.prev_time = 0.0
        self.clock = pygame.time.Clock()
        self.fps = deque()
        self.fps_depth = 60

    def game_loop(self):
        """update and render game every frame"""
        while self.running:
            self.get_dt()
            self.get_events()
            self.update()
            self.render()
        self.exit_requested = True

    def init_window(self):
        """Init pygame"""

        # Create pointers to directories
        self.assets_dir = os.path.join("assets")
        self.font_dir = os.path.join(self.assets_dir, "fonts")

        pygame.init()
        self.game_font = self.load_asset("font", "04B_30__.ttf", None, 30)
        self.title_font = self.load_asset("font", "04B_30__.ttf", None, 50)
        self.tech_font = self.load_asset("font", "Zector.ttf", None, 20)
        pygame.display.set_caption(GAME_NAME)

    def init_screen(self):
        """init screen"""
        # Screen and aspect ratio
        self.game_w = GAME_W
        self.game_h = GAME_H
        self.ratio = self.game_w / self.game_h

        self.screen_width = SCREEN_WIDTH
        self.screen_height = SCREEN_HEIGHT

        self.blit_origin = (0, 0)
        self.blit_w = self.screen_width
        self.blit_h = self.screen_height

        self.monitor_size = [
            pygame.display.Info().current_w,
            pygame.display.Info().current_h,
        ]

        logger.info(f"Monitor size: {self.monitor_size}")

        self.game_canvas = pygame.Surface((self.game_w, self.game_h))
        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height), pygame.RESIZABLE
        )

    def load_states(self, name):
        """Load current state for the game"""
        self.state = name

        match self.state:
            case "Title":
                title_menu = Title(name, self)
                title_menu.create_state()
            case _:
                logger.error(f"Unknown state: {self.state}")

        self.state = name
        logger.info(f"New state: {self.state}")
        logger.info(f"State list: {self.states}")

    def get_events(self):
        """get events such as mouse activity and windows events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        """Update canvas"""

    def render(self):
        """Render Canvas"""
        self.states[self.state].render()
        self.draw_fps()

        self.previous_game_canvas = self.game_canvas.copy()

        self.screen.blit(
            pygame.transform.scale(self.game_canvas, (self.blit_w, self.blit_h)),
            self.blit_origin,
        )
        pygame.display.flip()

    def get_dt(self):
        """get time between frames"""
        now = time.time()
        self.delta_time = now - self.prev_time
        self.prev_time = now
        self.fps.append(int(1 / self.delta_time))
        if len(self.fps) > self.fps_depth:
            self.fps.popleft()

    def draw_fps(self):
        """Draw Fps on screen"""
        if len(self.fps) == self.fps_depth:
            rect = pygame.Rect(0, 0, 50, 30)
            rect.topleft = (self.game_w - 55, self.game_h - 35)
            pygame.draw.rect(self.game_canvas, "black", rect)

            draw_text(
                self.game_canvas,
                str(int(sum(self.fps) / self.fps_depth)),
                "white",
                self.game_w - 10,
                self.game_h - 10,
                self.tech_font,
                "right",
            )

    def load_asset(self, asset_type, asset_name, asset_folder=None, asset_option=None):
        """Load various type of assets"""
        if asset_type in ["image", "font", "sound"]:
            logger.info(
                f"Loading {asset_type} asset: {asset_folder if asset_folder else ''}{'/' if asset_folder else ''}{asset_name} {asset_option if asset_option else ''}"
            )
        match asset_type:
            case "font":
                return pygame.font.Font(
                    os.path.join(self.font_dir, asset_name), asset_option
                )
            case _:
                logger.error(f"Unknown asset: {asset_type}")


if __name__ == "__main__":
    g = Game()
    while not g.exit_requested:
        g.game_loop()

        logger.info("Stopping")
        pygame.mixer.music.stop()
        pygame.quit()
        sys.exit()
