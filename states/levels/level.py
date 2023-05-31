""" level gameplay """

from states.state import State


class Level(State):
    def __init__(self, name, game):
        """init"""
        super().__init__(name, game)

    def update(self):
        """Update level state"""

    def render(self):
        """Render level"""
        self.game.game_canvas.fill("black")
