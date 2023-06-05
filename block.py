""" block object """


class Block:  # pylint: disable=R0903
    """Contains info of the block"""

    def __init__(self, value, block_type, show=True, animated=False):
        """init"""
        self.value = value
        self.show = show
        self.animated = animated
        self.cur_height = 0
        self.target_height = 0
        self.show_delay = 0
        self.block_type = block_type

    def __str__(self):
        return (
            f"[{self.value} show={self.show} animated={self.animated} "
            f"cur_height={self.cur_height} target_height={self.target_height} "
            f"delay={self.show_delay} block_type= {self.block_type}"
        )
