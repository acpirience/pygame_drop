""" level gameplay """
import pygame

from game_settings import GRID_COLOR, GRID_H, GRID_STEP, GRID_W, LEVEL_BG
from states.state import State


class Level(State):
    def __init__(self, name, game):
        """init"""
        super().__init__(name, game)
        self.margin_top = 128
        self.margin_left = 64

    def update(self):
        """Update level state"""

    def draw_grid(self):
        """draw the grid where the tile are placed"""
        for i in range(GRID_W + 1):
            pygame.draw.line(
                self.game.game_canvas,
                GRID_COLOR,
                (self.margin_left + i * (GRID_STEP + 1), self.margin_top),
                (
                    self.margin_left + i * (GRID_STEP + 1),
                    self.margin_top + 7 * GRID_STEP + 7,
                ),
            )
        for i in range(GRID_H + 1):
            pygame.draw.line(
                self.game.game_canvas,
                GRID_COLOR,
                (self.margin_left, self.margin_top + i * (GRID_STEP + 1)),
                (
                    self.margin_left + 7 * GRID_STEP + 7,
                    self.margin_top + i * (GRID_STEP + 1),
                ),
            )

    def render(self):
        """Render level"""
        self.game.game_canvas.fill(LEVEL_BG)
        self.draw_grid()
