import pygame
from objects import Paddle, Brick

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

WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)

BRICK_WIDTH: int = 150
BRICK_HEIGHT: int = 60
COLS: int = 8 
ROWS: int = 1
MARGIN: int = 8
START_X: int = 13
bricks: list[Brick] = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

paddle = Paddle(START_PADDLE, WHITE, PADDLE_VELOCITY)

for row in range(ROWS):
    for col in range(COLS):
        x = START_X + col * (BRICK_WIDTH + MARGIN)
        bricks.append(Brick(rect=pygame.Rect(x, 10, BRICK_WIDTH, BRICK_HEIGHT), color=RED))

def game():
    screen.fill(BLACK)
    paddle.draw(screen=screen)
    for brick in bricks:
        brick.draw(screen=screen)

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