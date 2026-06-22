import pygame
from dataclasses import dataclass

@dataclass
class Paddle:
    rect: pygame.Rect
    color: tuple[int, int, int]
    velocity_x: float

    def draw(self, screen):
        pygame.draw.rect(
            surface=screen, 
            color=self.color,
            rect=self.rect
        )