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


@dataclass
class Ball:
    color: tuple[int, int, int]
    center: tuple[int, int]
    radius: int

    def get_rect(self) -> pygame.Rect:
        return pygame.Rect(
            self.center[0] - self.radius,
            self.center[1] - self.radius,
            self.radius * 2,
            self.radius * 2
        )

    def draw(self, screen):
        pygame.draw.circle(
            surface=screen,
            color=self.color,
            center=self.center,
            radius=self.radius
        )