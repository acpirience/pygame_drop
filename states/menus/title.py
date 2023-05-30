""" Home page and main menu of the game  """

from states.state import State
from utils import draw_text


class Title(State):
    """Home page and main menu of the game"""

    def __init__(self, name, game):  # pylint: disable=W0246
        """Init title"""
        super().__init__(name, game)

    def draw_title(self):
        """Draw title on Home screen"""
        draw_text(
            self.game.game_canvas,
            "Drop 7 Clone",
            "white",
            (self.game.game_w / 2),
            (self.game.game_h / 6),
            self.game.title_font,
        )

    def update(self):
        """Update statutes of screen"""

    def render(self):
        """Render screen"""
        self.game.game_canvas.fill("black")
        self.draw_title()
