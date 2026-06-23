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


@dataclass
class Brick:
    rect: pygame.Rect
    color: tuple[int, int, int]
    hp: int = 1

    def draw(self, screen):
        pygame.draw.rect(
            surface=screen,
            color=self.color,
            rect=self.rect
        )