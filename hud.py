import pygame
from settings import SCREEN_W


def draw_hud(
    screen: pygame.Surface,
    players,
    osg_score: int,
    font: pygame.font.Font,
) -> None:
    """Draw the in-game score overlay (SCR-05).

    Superman top-left, Goblin top-right,
    OmnipotentShootingGuy top-center (hidden when 0).
    """
    def _blit(text: str, x: int, y: int, anchor: str = "left") -> None:
        shadow = font.render(text, True, (0, 0, 0))
        surf   = font.render(text, True, (255, 255, 255))
        if anchor == "right":
            screen.blit(shadow, (x - shadow.get_width() + 2, y + 2))
            screen.blit(surf,   (x - surf.get_width(),       y))
        elif anchor == "center":
            screen.blit(shadow, (x - shadow.get_width() // 2 + 2, y + 2))
            screen.blit(surf,   (x - surf.get_width() // 2,       y))
        else:
            screen.blit(shadow, (x + 2, y + 2))
            screen.blit(surf,   (x,     y))

    sup, gob = players[0], players[1]
    _blit(f"Superman: {sup.score}",  10,          10, "left")
    _blit(f"Goblin: {gob.score}",    SCREEN_W - 10, 10, "right")
    if osg_score > 0:
        _blit(f"OmnipotentShootingGuy: {osg_score}", SCREEN_W // 2, 10, "center")
