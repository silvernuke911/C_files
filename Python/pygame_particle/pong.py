import pygame
import sys

# Initialization
pygame.init()
pygame.display.set_caption("Pong")
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont("Consolas", 24)
clock = pygame.time.Clock()
vec2 = pygame.math.Vector2
background_color = (10, 10, 10)

# Constants
WIDTH, HEIGHT = screen.get_size()
PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
BALL_RADIUS = 10
BALL_SPEED = 6
PADDLE_SPEED = 6

# Ball class
class Ball:
    def __init__(self, pos):
        self.pos = vec2(pos)
        self.vel = vec2(BALL_SPEED, BALL_SPEED)
        self.radius = BALL_RADIUS
        self.color = (255, 255, 255)

    def update(self, paddle1, paddle2):
        self.pos += self.vel

        # Top and bottom bounce
        if self.pos.y - self.radius <= 0 or self.pos.y + self.radius >= HEIGHT:
            self.vel.y *= -1

        # Left paddle bounce
        if (
            paddle1.left <= self.pos.x - self.radius <= paddle1.right and
            paddle1.top <= self.pos.y <= paddle1.bottom
        ):
            self.vel.x *= -1

        # Right paddle bounce
        if (
            paddle2.left <= self.pos.x + self.radius <= paddle2.right and
            paddle2.top <= self.pos.y <= paddle2.bottom
        ):
            self.vel.x *= -1

        # Reset if out of bounds
        if self.pos.x < 0 or self.pos.x > WIDTH:
            self.pos = vec2(WIDTH // 2, HEIGHT // 2)
            self.vel = vec2(BALL_SPEED * (-1 if self.vel.x > 0 else 1), BALL_SPEED)

    def draw(self, surface):
        pygame.draw.circle(surface, self.color, self.pos, self.radius)

# Paddle class
class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = (255, 255, 255)

    def move(self, dy):
        self.rect.y += dy
        self.rect.y = max(0, min(HEIGHT - PADDLE_HEIGHT, self.rect.y))

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

    @property
    def top(self):
        return self.rect.top

    @property
    def bottom(self):
        return self.rect.bottom

    @property
    def left(self):
        return self.rect.left

    @property
    def right(self):
        return self.rect.right

# Game objects
ball = Ball((WIDTH // 2, HEIGHT // 2))
paddle_left = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2)
paddle_right = Paddle(WIDTH - 60, HEIGHT // 2 - PADDLE_HEIGHT // 2)

# Game loop
running = True
while running:
    screen.fill(background_color)
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player control (W/S)
    if keys[pygame.K_w]:
        paddle_left.move(-PADDLE_SPEED)
    if keys[pygame.K_s]:
        paddle_left.move(PADDLE_SPEED)

    # AI or second player (UP/DOWN)
    if keys[pygame.K_UP]:
        paddle_right.move(-PADDLE_SPEED)
    if keys[pygame.K_DOWN]:
        paddle_right.move(PADDLE_SPEED)

    # Update game state
    ball.update(paddle_left.rect, paddle_right.rect)

    # Draw everything
    ball.draw(screen)
    paddle_left.draw(screen)
    paddle_right.draw(screen)

    # Flip and tick
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Pong Menu")
font = pygame.font.SysFont("Consolas", 36)
clock = pygame.time.Clock()
vec2 = pygame.math.Vector2

# Button class reused
class Button:
    def __init__(self, rect, text, font, bg_color, text_color, hover_color):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event):
        return self.hovered and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1

# Menu function
def menu():
    play_button = Button((300, 250, 200, 60), "PLAY", font, (30, 30, 30), (255, 255, 255), (60, 60, 60))
    quit_button = Button((300, 340, 200, 60), "QUIT", font, (30, 30, 30), (255, 255, 255), (60, 60, 60))

    while True:
        screen.fill((10, 10, 10))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if play_button.is_clicked(event):
                return  # Exit the menu and start the game
            if quit_button.is_clicked(event):
                pygame.quit()
                sys.exit()

        play_button.update(mouse_pos)
        quit_button.update(mouse_pos)
        play_button.draw(screen)
        quit_button.draw(screen)

        title = font.render("Welcome to Pong!", True, (255, 255, 255))
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 150))

        pygame.display.flip()
        clock.tick(60)

# Your actual game code goes here
def main_game():
    # Insert your pong game loop here
    running = True
    while running:
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Replace this with real drawing
        text = font.render("Game Running... Press ESC to quit", True, (255, 255, 255))
        screen.blit(text, (100, 100))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_ESCAPE]:
            running = False

        pygame.display.flip()
        clock.tick(60)

# Run the menu, then the game
menu()
main_game()
pygame.quit()
sys.exit()
