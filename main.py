import pygame
from objects import Paddle, Brick, Ball, Button

pygame.init()

#SCREEN
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 1200

# PADDLE
PADDLE_HEIGHT = 10
PADDLE_WIDTH = 180
START_PADDLE = pygame.Rect(
    SCREEN_WIDTH // 2, 
    (SCREEN_HEIGHT - PADDLE_HEIGHT) - SCREEN_HEIGHT // 4,
    PADDLE_WIDTH,
    PADDLE_HEIGHT
)
PADDLE_VELOCITY = 10

#COLORS
WHITE: tuple[int, int, int] = (255, 255, 255)
BLACK: tuple[int, int, int] = (0, 0, 0)
RED: tuple[int, int, int] = (255, 0, 0)
PINK: tuple[int, int, int] = (255, 102, 178)
BLUE: tuple[int, int, int] = (0, 0, 255)

#BRICK
BRICK_WIDTH: int = 110
BRICK_HEIGHT: int = 50
COLS: int = 8 
ROWS: int = 6
MARGIN_LEFT: int = 8
MARGIN_TOP: int = 8
START_X: int = (SCREEN_WIDTH - (MARGIN_LEFT * 8 + BRICK_WIDTH * 8)) // 2
START_Y: int = 20
bricks: list[Brick] = []

#MENU_BUTTONS
BUTTON_WIDTH = SCREEN_WIDTH // 3
BUTTON_HEIGHT = SCREEN_HEIGHT // 12
START_BUTTON_POSITION = pygame.Rect(
    SCREEN_WIDTH // 3,
    SCREEN_HEIGHT // 12,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
EXIT_BUTTON_POSITION = pygame.Rect(
    SCREEN_WIDTH // 3,
    SCREEN_HEIGHT // 12 + 3 * BUTTON_HEIGHT,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

GAME_STATES: tuple[str, str, str] = ('menu', 'game', 'loss')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_state = GAME_STATES[0]

paddle = Paddle(START_PADDLE, WHITE, PADDLE_VELOCITY)
ball = Ball(PINK, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 12)
play_button = Button(START_BUTTON_POSITION, BLUE)
exit_button = Button(EXIT_BUTTON_POSITION, BLUE)

for row in range(ROWS):
    for col in range(COLS):
        x = START_X + col * (BRICK_WIDTH + MARGIN_LEFT)
        y = START_Y + row * (BRICK_HEIGHT + MARGIN_TOP)
        bricks.append(Brick(rect=pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT), color=RED))

def render_menu():
    screen.fill(BLACK)
    play_button.draw(screen=screen)
    exit_button.draw(screen=screen)

def render_game():

    bricks[:] = [brick for brick in bricks if brick.hp]
    ball.move()

    screen.fill(BLACK)
    paddle.draw(screen=screen)
    ball.draw(screen=screen)

    if paddle.rect.colliderect(ball.get_rect()):
        ball.velocity_y *= -1
    
    if ball.center[0] <= ball.radius or ball.center[0] >= SCREEN_WIDTH - ball.radius:
        ball.velocity_x *= -1

    for brick in bricks:
        if brick.hp:
            brick.draw(screen=screen)
        if brick.rect.colliderect(ball.get_rect()):
            brick.hp = 0
            ball_center_x = ball.center[0]
            ball_center_y = ball.center[1]
            brick_center_x = brick.rect.centerx
            brick_center_y = brick.rect.centery

            dx = ball_center_x - brick_center_x
            dy = ball_center_y - brick_center_y

            if abs(dx) > abs(dy):
                ball.velocity_x *= -1
                if dx > 0:
                    ball_center_x = brick.rect.right + ball.radius
                else:
                    ball_center_x = brick.rect.left - ball.radius
            else:
                ball.velocity_y *= -1
                if dy > 0:
                    ball_center_y = brick.rect.bottom + ball.radius
                else:
                    ball_center_y = brick.rect.top - ball.radius


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
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.Rect.collidepoint(play_button.rect, pygame.mouse.get_pos()):
                    game_state = GAME_STATES[1]
                if pygame.Rect.collidepoint(exit_button.rect, pygame.mouse.get_pos()):
                    running = False

        # render game start

        if game_state == 'menu':
            render_menu()
        if game_state == 'game':
            render_game()
        

        # render game end

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()