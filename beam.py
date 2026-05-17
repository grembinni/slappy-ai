import pygame
from settings import (
    BEAM_LENGTH, BEAM_WIDTH, BEAM_SPEED, SCREEN_W,
    DIR_LEFT, DIR_RIGHT,
)


class Beam:
    def __init__(self, x: float, y: float, direction: int, color: tuple) -> None:
        self.x = float(x)       # leading-edge x (leftmost for DIR_LEFT, rightmost for DIR_RIGHT)
        self.y = float(y)       # vertical center — beam is a horizontal line
        self.direction = direction
        self.color = color
        self.distance_traveled: float = 0.0

    @property
    def start(self) -> tuple:
        """Left endpoint of the 40px bolt segment."""
        if self.direction == DIR_LEFT:
            return (int(self.x), int(self.y))
        return (int(self.x - BEAM_LENGTH), int(self.y))

    @property
    def end(self) -> tuple:
        """Right endpoint of the 40px bolt segment."""
        if self.direction == DIR_LEFT:
            return (int(self.x + BEAM_LENGTH), int(self.y))
        return (int(self.x), int(self.y))

    def update(self, dt: float) -> bool:
        """Advance beam by dt seconds. Returns True while alive, False when expired."""
        if self.direction == DIR_LEFT:
            self.x -= BEAM_SPEED * dt
        else:
            self.x += BEAM_SPEED * dt
        self.distance_traveled += BEAM_SPEED * dt
        # Horizontal wrap (D-06)
        if self.x < -BEAM_LENGTH:
            self.x = float(SCREEN_W)
        elif self.x > SCREEN_W:
            self.x = float(-BEAM_LENGTH)
        # Expire after 1 full screen width (beam dies before looping back to origin)
        return self.distance_traveled < SCREEN_W

    def draw(self, screen: pygame.Surface) -> None:
        """Draw the beam as a colored line on screen."""
        pygame.draw.line(screen, self.color, self.start, self.end, BEAM_WIDTH)
