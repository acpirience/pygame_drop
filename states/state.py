""" Handle states storing for the game """


class State:
    """Alle game states derive from this class"""

    def __init__(self, name, game):
        """Init state"""
        self.game = game
        self.name = name

    def update(self, delta_time, actions):
        """Update state"""

    def render(self):
        """Render state"""

    def create_state(self):
        """Create state"""
        self.game.states[self.name] = self
