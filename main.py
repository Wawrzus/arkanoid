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

#FONT
font = pygame.font.SysFont('Arial', 30)
play_text_surface = font.render('start', True, WHITE)
exit_text_surface = font.render('exit', True, WHITE)
loss_text_surface = font.render('loss', True, WHITE)
win_text_surface = font.render('win', True, WHITE)

#BRICK
BRICK_WIDTH: int = 110
BRICK_HEIGHT: int = 50
COLS: int = 8 
ROWS: int = 1
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
    SCREEN_HEIGHT // 3,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)
EXIT_BUTTON_POSITION = pygame.Rect(
    SCREEN_WIDTH // 3,
    SCREEN_HEIGHT // 3 + 2 * BUTTON_HEIGHT,
    BUTTON_WIDTH,
    BUTTON_HEIGHT
)

GAME_STATES: tuple[str, str, str] = ('menu', 'game', 'loss', 'win')

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()
running = True
game_state = GAME_STATES[0]

paddle = Paddle(START_PADDLE, WHITE, PADDLE_VELOCITY)
ball = Ball(PINK, [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2], 12)
play_button = Button(START_BUTTON_POSITION, BLUE)
exit_button = Button(EXIT_BUTTON_POSITION, BLUE)
play_rect_text = play_text_surface.get_rect(center=(play_button.rect.centerx, play_button.rect.centery))
exit_rect_text = exit_text_surface.get_rect(center=(exit_button.rect.centerx, exit_button.rect.centery))
loss_rect_text = loss_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
win_rect_text = win_text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

def _create_bricks(bricks: list[Brick]):
    for row in range(ROWS):
        for col in range(COLS):
            x = START_X + col * (BRICK_WIDTH + MARGIN_LEFT)
            y = START_Y + row * (BRICK_HEIGHT + MARGIN_TOP)
            bricks.append(Brick(rect=pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT), color=RED))

_create_bricks(bricks=bricks)

def render_loss():
    screen.fill(BLACK)
    screen.blit(loss_text_surface, loss_rect_text)

def render_win():
    screen.fill(BLACK)
    screen.blit(win_text_surface, win_rect_text)

def render_menu():
    screen.fill(BLACK)
    play_button.draw(screen=screen)
    screen.blit(play_text_surface, play_rect_text)
    exit_button.draw(screen=screen)
    screen.blit(exit_text_surface, exit_rect_text)

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

    if ball.center[1] - ball.radius <= 0:
        ball.velocity_y *= -1

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

        if not bricks and game_state != GAME_STATES[3]:
            start = pygame.time.get_ticks()
            game_state = GAME_STATES[3]
            _create_bricks(bricks=bricks)
            ball.center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

        if ball.center[1] > SCREEN_HEIGHT and game_state != GAME_STATES[2]:
            start = pygame.time.get_ticks()
            game_state = GAME_STATES[2]
            ball.center = [SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2]

        if game_state == GAME_STATES[2] and pygame.time.get_ticks() - start > 2000:
            game_state = GAME_STATES[0]

        if game_state == GAME_STATES[3] and pygame.time.get_ticks() - start > 2000:
            game_state = GAME_STATES[0]

        if game_state == 'menu':
            render_menu()
        if game_state == 'game':
            render_game()
        if game_state == 'loss':
            render_loss()
        if game_state == 'win':
            render_win()

        # render game end

        pygame.display.flip()
        clock.tick(120)

    pygame.quit()