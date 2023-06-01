""" level gameplay """
import pygame
from loguru import logger

from game_settings import (
    GRID_COLOR,
    GRID_H,
    GRID_HIGHLIGHT,
    GRID_STEP,
    GRID_W,
    LEVEL_BG,
    NB_BLOCKS,
)
from states.state import State
from utils import draw_rect


class Level(State):
    def __init__(self, name, game):
        """init"""
        super().__init__(name, game)
        self.margin_top = 128
        self.margin_left = 64
        self.blocks = {"unknown": None}
        for i in range(NB_BLOCKS):
            self.blocks[f"{i+1}"] = None
        logger.info(f"Grid is {GRID_W}x{GRID_H}")
        self.load_assets()

    def load_assets(self):
        for key in self.blocks:
            self.blocks[key] = self.game.load_asset("image", f"block_{key}.png")

    def update(self):
        """Update level state"""

    def mouse_on_column(self):
        if (
            self.game.mouse_y < self.margin_top - 30
            or self.game.mouse_y > self.margin_top + GRID_H * GRID_STEP + 7
        ):
            return None
        if (
            self.game.mouse_x < self.margin_left
            or self.game.mouse_x > self.margin_left + GRID_W * GRID_STEP + 7
        ):
            return None

        for i in range(GRID_W):
            if (
                self.margin_left + i * (GRID_STEP + 1)
                < self.game.mouse_x
                < self.margin_left + (i + 1) * (GRID_STEP + 1)
            ):
                return i

    def draw_grid(self):
        """draw the grid where the tile are placed"""
        for i in range(GRID_W + 1):
            pygame.draw.line(
                self.game.game_canvas,
                GRID_COLOR,
                (self.margin_left + i * (GRID_STEP + 1), self.margin_top),
                (
                    self.margin_left + i * (GRID_STEP + 1),
                    self.margin_top + GRID_H * GRID_STEP + GRID_H,
                ),
            )
        for i in range(GRID_H + 1):
            pygame.draw.line(
                self.game.game_canvas,
                GRID_COLOR,
                (self.margin_left, self.margin_top + i * (GRID_STEP + 1)),
                (
                    self.margin_left + GRID_W * GRID_STEP + GRID_W,
                    self.margin_top + i * (GRID_STEP + 1),
                ),
            )

    def draw_highlight(self, col):
        rect = pygame.Rect(
            0,
            0,
            GRID_STEP + 2,
            GRID_H * GRID_STEP + GRID_H + 30,
        )
        draw_rect(
            self.game.game_canvas,
            rect,
            self.margin_left + col * (GRID_STEP + 1),
            self.margin_top + GRID_H * GRID_STEP + GRID_H,
            GRID_HIGHLIGHT,
            10,
        )

    def draw_block(self, grid_x, grid_y, block):
        pos_x = self.margin_left + grid_x * (GRID_STEP + 1) + 1
        pos_y = self.margin_top + grid_y * (GRID_STEP + 1) + 1
        self.game.game_canvas.blit(self.blocks[block], (pos_x, pos_y))

    def render(self):
        """Render level"""
        block = 0
        self.game.game_canvas.fill(LEVEL_BG)
        selected_col = self.mouse_on_column()
        if selected_col is not None:
            self.draw_highlight(selected_col)
        self.draw_grid()
        for y in range(GRID_H):
            for x in range(GRID_W):
                if block % len(self.blocks) == 0:
                    self.draw_block(x, y, "unknown")
                else:
                    self.draw_block(x, y, f"{block % len(self.blocks)}")
                block += 1
