import pygame
from objects import Paddle

pygame.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720

PADDLE_HEIGHT = 10
PADDLE_WIDTH = 200
START_PADDLE = pygame.Rect(
    SCREEN_WIDTH // 2, 
    SCREEN_HEIGHT - PADDLE_HEIGHT,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)
PADDLE_VELOCITY = 10

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

paddle = Paddle(START_PADDLE, WHITE, PADDLE_VELOCITY)

def game():
    screen.fill(BLACK)
    paddle.draw(screen=screen)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a] and paddle.rect.left >= 0:
        paddle.rect.x -= paddle.velocity_x
    if keys[pygame.K_d] and paddle.rect.right <= SCREEN_WIDTH:
        paddle.rect.x += paddle.velocity_x


if __name__ == "__main__":
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # render game start

        game()

        # render game end

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()