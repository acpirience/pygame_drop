""" utilities functions used by the game  """


def draw_text(
    surface, text, color, pos_x, pos_y, font, align="center"
):  # pylint: disable=R0913
    """Draws a string on the screen"""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    match align:
        case "center":
            text_rect.center = (pos_x, pos_y)
        case "left":
            text_rect.bottomleft = (pos_x, pos_y)
        case "right":
            text_rect.bottomright = (pos_x, pos_y)
    surface.blit(text_surface, text_rect)
