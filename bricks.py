import pygame
import sys

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Brick Breaker")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for controlling the frame rate
clock = pygame.time.Clock()
FPS = 60

# Paddle properties
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
PADDLE_SPEED = 7
paddle = pygame.Rect(WIDTH // 2 - PADDLE_WIDTH // 2, HEIGHT - 30, PADDLE_WIDTH, PADDLE_HEIGHT)

# Ball properties
BALL_RADIUS = 8
ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
ball_dx, ball_dy = 4, -4

# Brick properties
BRICK_WIDTH = 75
BRICK_HEIGHT = 20
BRICK_ROWS = 5
BRICK_COLS = 10
bricks = []

for row in range(BRICK_ROWS):
    for col in range(BRICK_COLS):
        brick_x = col * (BRICK_WIDTH + 5) + 35
        brick_y = row * (BRICK_HEIGHT + 5) + 50
        bricks.append(pygame.Rect(brick_x, brick_y, BRICK_WIDTH, BRICK_HEIGHT))

# Score and lives
score = 0
lives = 3
font = pygame.font.Font(None, 36)

# Game loop
def game_loop():
    global ball, ball_dx, ball_dy, score, lives, bricks

    running = True
    while running:
        screen.fill(BLACK)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Move paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle.left > 0:
            paddle.move_ip(-PADDLE_SPEED, 0)
        if keys[pygame.K_RIGHT] and paddle.right < WIDTH:
            paddle.move_ip(PADDLE_SPEED, 0)

        # Move ball
        ball.move_ip(ball_dx, ball_dy)

        # Ball collision with walls
        if ball.left <= 0 or ball.right >= WIDTH:
            ball_dx = -ball_dx
        if ball.top <= 0:
            ball_dy = -ball_dy

        # Ball collision with paddle
        if ball.colliderect(paddle):
            ball_dy = -ball_dy

        # Ball collision with bricks
        for brick in bricks[:]:
            if ball.colliderect(brick):
                bricks.remove(brick)
                ball_dy = -ball_dy
                score += 10
                break

        # Ball out of bounds
        if ball.bottom >= HEIGHT:
            lives -= 1
            ball = pygame.Rect(WIDTH // 2, HEIGHT // 2, BALL_RADIUS, BALL_RADIUS)
            ball_dx, ball_dy = 4, -4
            if lives == 0:
                running = False

        # Draw paddle, ball, bricks, and text
        pygame.draw.rect(screen, WHITE, paddle)
        pygame.draw.ellipse(screen, RED, ball)

        for brick in bricks:
            pygame.draw.rect(screen, BLUE, brick)

        score_text = font.render(f"Score: {score}", True, WHITE)
        lives_text = font.render(f"Lives: {lives}", True, WHITE)
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (WIDTH - 100, 10))

        # Win condition
        if not bricks:
            win_text = font.render("You Win!", True, WHITE)
            screen.blit(win_text, (WIDTH // 2 - 50, HEIGHT // 2))
            pygame.display.flip()
            pygame.time.delay(3000)
            running = False

        # Update display and tick clock
        pygame.display.flip()
        clock.tick(FPS)

# Run the game
game_loop()
pygame.quit()
