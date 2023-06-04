""" level gameplay """
from random import randrange

import pygame
from loguru import logger

from block import Block
from game_settings import (
    DROP_INTERVAL,
    DROP_SPEED,
    GRID_COLOR,
    GRID_H,
    GRID_HIGHLIGHT,
    GRID_STEP,
    GRID_W,
    LEVEL_BG,
    MAX_START_BLOCK,
    MIN_START_BLOCK,
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
        self.blocks = {0: None}
        for i in range(NB_BLOCKS):
            self.blocks[i + 1] = None
        logger.info(f"Grid is {GRID_W}x{GRID_H}")
        self.grid_content = [[None for _ in range(GRID_H)] for _ in range(GRID_W)]
        self.next_block = None
        self.block_is_falling = False
        self.init_grid()
        self.init_animate_grid()
        self.load_assets()

    def load_assets(self):
        for key in self.blocks:
            self.blocks[key] = self.game.load_asset("image", f"block_{key}.png")

    def init_grid(self):
        """init grid"""
        nb = randrange(MIN_START_BLOCK, MAX_START_BLOCK)
        for _ in range(nb):
            col = randrange(GRID_W)
            block = randrange(NB_BLOCKS)
            self.drop_block(col, block)

    def drop_block(self, col, block):
        for y in reversed(range(GRID_H)):
            if self.grid_content[col][y] is None:
                self.grid_content[col][y] = Block(block, False, False)
                break

    def init_animate_grid(self):
        """draw initial grid with animated falling block"""
        nb_blocks = 0
        for y in reversed(range(GRID_H)):
            for x in range(GRID_W):
                if self.grid_content[x][y] is not None:
                    self.grid_content[x][y].cur_height = -1.25
                    self.grid_content[x][y].target_height = y
                    self.grid_content[x][y].show = True
                    self.grid_content[x][y].animated = True
                    self.grid_content[x][y].show_delay = nb_blocks * 10
                    nb_blocks += 1

    @property
    def max_height(self):
        """give the highest block on the grid to deal"""
        max_height = 0
        for x in range(GRID_W):
            for y in reversed(range(GRID_H)):
                if self.grid_content[x][y] is None:
                    if GRID_H - y > max_height:
                        max_height = GRID_H - y
                    break
        return max_height - 1

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
            GRID_H * GRID_STEP + GRID_H + 10,
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
        self.game.game_canvas.blit(self.blocks[block.value], (pos_x, pos_y))

    def update(self):
        """Update level state"""
        self.block_is_falling = False
        for x in range(GRID_W):
            for y in reversed(range(GRID_H)):
                if (
                    self.grid_content[x][y] is not None
                    and self.grid_content[x][y].animated
                ):
                    if self.grid_content[x][y].show_delay >= 0:
                        self.grid_content[x][y].show_delay -= (
                            self.game.delta_time * DROP_INTERVAL
                        )
                    else:
                        self.grid_content[x][y].cur_height += (
                            DROP_SPEED * self.game.delta_time
                        )
                        self.block_is_falling = True
                        if (
                            self.grid_content[x][y].cur_height
                            >= self.grid_content[x][y].target_height
                        ):
                            self.grid_content[x][y].cur_height = 0
                            self.grid_content[x][y].target_height = 0
                            self.grid_content[x][y].animated = False

    def render(self):
        """Render level"""
        self.next_block = None
        if not self.block_is_falling:  # if no block is falling, show next block
            self.next_block = Block(6, True, False)
        self.game.game_canvas.fill(LEVEL_BG)
        selected_col = self.mouse_on_column()
        if selected_col is not None:
            self.draw_highlight(selected_col)
            if self.next_block is not None:
                self.draw_block(selected_col, -1.25, self.next_block)
        self.draw_grid()
        for y in range(GRID_H):
            for x in range(GRID_W):
                cur_block = self.grid_content[x][y]
                if cur_block is not None:
                    if cur_block.show and cur_block.show_delay <= 0:
                        if cur_block.animated:
                            self.draw_block(x, cur_block.cur_height, cur_block)
                        else:
                            self.draw_block(x, y, cur_block)
