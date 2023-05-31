""" Home page and main menu of the game  """

import pygame

from game_settings import GAME_NAME, MENU_BG, MENU_COLOUR, SELECT_COLOUR
from states.state import State
from utils import draw_rect, draw_text


class Title(State):
    """Home page and main menu of the game"""

    def __init__(self, name, game):  # pylint: disable=W0246
        """Init title"""
        super().__init__(name, game)
        self.menu_items = ["Play"]
        self.selected_item = None
        self.menu_start_w = (self.game.game_w * 0.5) - 50
        self.menu_start_h = self.game.game_h * 0.4
        self.menu_offset = 80
        self.active = None

    def draw_title(self):
        """Draw title on Home screen"""
        draw_text(
            self.game.game_canvas,
            GAME_NAME,
            MENU_COLOUR,
            (self.game.game_w / 2),
            (self.game.game_h / 6),
            self.game.title_font,
        )

    def draw_menu(self):
        """draw main menu"""
        for i, item in enumerate(self.menu_items):
            menu_x = self.menu_start_w - 10
            menu_y = self.menu_start_h + i * self.menu_offset + 10.0
            text_width = self.game.game_font.size(item)[0]
            if self.mouse_in(menu_x, menu_y, text_width + 20, 55):
                rect = pygame.Rect(0, 0, text_width + 20, 55)
                draw_rect(
                    self.game.game_canvas,
                    rect,
                    menu_x,
                    menu_y,
                    SELECT_COLOUR,
                    10,
                )

            draw_text(
                self.game.game_canvas,
                item,
                MENU_COLOUR,
                self.menu_start_w,
                self.menu_start_h + i * self.menu_offset,
                self.game.game_font,
                "left",
            )

    def mouse_in(self, rect_x, rect_y, width, height):
        """returns True if mouse is in rectangle given"""
        return (
            rect_x < self.game.mouse_x < rect_x + width
            and rect_y - height < self.game.mouse_y < rect_y
        )

    def update(self, delta_time, actions):
        """Update statutes of screen"""

    def render(self):
        """Render screen"""
        self.game.game_canvas.fill(MENU_BG)
        self.draw_title()
        self.draw_menu()
