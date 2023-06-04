""" block object """


class Block:  # pylint: disable=R0903
    """Contains info of the block"""

    def __init__(self, value, show=True, animated=False):
        """init"""
        self.value = value
        self.show = show
        self.animated = animated
        self.cur_height = 0
        self.target_height = 0
        self.show_delay = 0

    def __str__(self):
        return f"[{self.value} show={self.show} animated={self.animated} cur_height={self.cur_height} target_height= {self.target_height} delay={self.show_delay}"
