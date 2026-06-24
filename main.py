import pygame
from objects import Paddle, Brick

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1200

PADDLE_HEIGHT = 10
PADDLE_WIDTH = 200
START_PADDLE = pygame.Rect(
    SCREEN_WIDTH // 2, 
    (SCREEN_HEIGHT - PADDLE_HEIGHT) - SCREEN_HEIGHT // 4,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)
PADDLE_VELOCITY = 10

WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)

BRICK_WIDTH: int = 110
BRICK_HEIGHT: int = 50
COLS: int = 8 
ROWS: int = 5
MARGIN_LEFT: int = 8
MARGIN_TOP: int = 8
START_X: int = (SCREEN_WIDTH - (MARGIN_LEFT * 8 + BRICK_WIDTH * 8)) / 2
START_Y: int = 20
bricks: list[Brick] = []

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True

paddle = Paddle(START_PADDLE, WHITE, PADDLE_VELOCITY)

for row in range(ROWS):
    for col in range(COLS):
        x = START_X + col * (BRICK_WIDTH + MARGIN_LEFT)
        y = START_Y + row * (BRICK_HEIGHT + MARGIN_TOP)
        bricks.append(Brick(rect=pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT), color=RED))

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