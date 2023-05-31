""" utilities functions used by the game  """

import pygame


def draw_rect(
    canvas, rect, pos_x, pos_y, colour, border_radius=0
):  # pylint: disable=R0913
    """Draws a rectangle on the screen"""
    rect.bottomleft = (pos_x, pos_y)
    pygame.draw.rect(canvas, colour, rect, 0, border_radius)


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
