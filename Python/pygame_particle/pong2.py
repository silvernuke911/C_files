import pygame
import sys
import random
from typing import Tuple

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 500
PADDLE_WIDTH, PADDLE_HEIGHT = 20, 100
PADDLE_SPEED = 10
BALL_RADIUS = 10
BACKGROUND_COLOR = (10, 10, 10)
WHITE = (255, 255, 255)

class Ball:
    def __init__(self, pos: Tuple[int, int], vel: Tuple[int, int]):
        self.pos = pygame.math.Vector2(pos)
        self.vel = pygame.math.Vector2(vel)
        self.radius = BALL_RADIUS
        self.color = WHITE
        self.reset_pos = pygame.math.Vector2(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

    def update(self, paddle1: 'Paddle', paddle2: 'Paddle') -> Tuple[int, int]:
        """Update ball position and handle collisions. Returns scoring (left, right)."""
        self.pos += self.vel

        # Wall collision
        if self.pos.y - self.radius <= 0 or self.pos.y + self.radius >= SCREEN_HEIGHT:
            self.vel.y *= -1

        # Paddle collisions
        if self._check_paddle_collision(paddle1):
            self.vel.x = abs(self.vel.x)  # Ensure ball moves right
            self.vel.y += paddle1.vel_y 

        if self._check_paddle_collision(paddle2):
            self.vel.x = -abs(self.vel.x)  # Ensure ball moves left
            self.vel.y += paddle2.vel_y 

        # Scoring
        if self.pos.x < 0:
            self.reset()
            return (0, 1)
        if self.pos.x > SCREEN_WIDTH:
            self.reset()
            return (1, 0)
        
        return (0, 0)

    def _check_paddle_collision(self, paddle: 'Paddle') -> bool:
        """Check if ball collides with given paddle, considering which side to check based on paddle position."""
        if paddle.left < SCREEN_WIDTH / 2:  # Left paddle
            # Check right side of ball against left paddle
            return (paddle.left <= self.pos.x + self.radius <= paddle.right and
                    paddle.top <= self.pos.y <= paddle.bottom)
        else:  # Right paddle
            # Check left side of ball against right paddle
            return (paddle.left <= self.pos.x - self.radius <= paddle.right and
                    paddle.top <= self.pos.y <= paddle.bottom)

    def reset(self):
        """Reset ball to center with random direction."""
        self.pos = self.reset_pos.copy()
        self.vel = pygame.math.Vector2(
            6 * (-1 if random.random() < 0.5 else 1),
            random.uniform(-3, 3)
        )

    def draw(self, surface: pygame.Surface):
        pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)


class Paddle:
    def __init__(self, x: int, y: int):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.color = WHITE
        self.last_y = y
        self.vel_y = 0

    def move(self, dy: int):
        """Move paddle with boundary checking."""
        self.last_y = self.rect.y
        self.rect.y = max(0, min(SCREEN_HEIGHT - PADDLE_HEIGHT, self.rect.y + dy))
        self.vel_y = self.rect.y - self.last_y

    def draw(self, surface: pygame.Surface):
        pygame.draw.rect(surface, self.color, self.rect)

    @property
    def top(self) -> int:
        return self.rect.top

    @property
    def bottom(self) -> int:
        return self.rect.bottom

    @property
    def left(self) -> int:
        return self.rect.left

    @property
    def right(self) -> int:
        return self.rect.right

    @property
    def centerx(self) -> int:
        return self.rect.centerx


class Button:
    def __init__(self, rect: Tuple[int, int, int, int], text: str, 
                 font_name: str, font_size: int, 
                 bg_color: Tuple[int, int, int], text_color: Tuple[int, int, int], 
                 hover_color: Tuple[int, int, int]):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bg_color = bg_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (200, 200, 200), self.rect, 2)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos: Tuple[int, int]):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (self.hovered and 
                event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1)


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Pong")
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        
        # Game objects
        self.ball = Ball((SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), (6, 0))
        self.paddle_left = Paddle(50, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        self.paddle_right = Paddle(SCREEN_WIDTH - 70, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2)
        
        # Game state
        self.score_left = 0
        self.score_right = 0
        self.font = pygame.font.SysFont("Consolas", 20)
        self.score_font = pygame.font.SysFont("Consolas", 36)
        self.title_font = pygame.font.SysFont("Consolas", 72)

    def run(self):
        """Run the game loop."""
        self.show_menu()
        self.main_game()

    def show_menu(self):
        """Display the main menu."""
        play_button = Button(
            (300, 250, 200, 60), "PLAY", "Consolas", 20,
            (30, 30, 30), WHITE, (60, 60, 60)
        )
        quit_button = Button(
            (300, 340, 200, 60), "QUIT", "Consolas", 20,
            (30, 30, 30), WHITE, (60, 60, 60)
        )

        while True:
            self.screen.fill(BACKGROUND_COLOR)
            mouse_pos = pygame.mouse.get_pos()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.quit()
                if play_button.is_clicked(event):
                    return
                if quit_button.is_clicked(event):
                    self.quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    return

            play_button.update(mouse_pos)
            quit_button.update(mouse_pos)
            
            # Draw menu elements
            play_button.draw(self.screen)
            quit_button.draw(self.screen)
            
            title = self.title_font.render("PONG!", True, WHITE)
            self.screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 150))

            pygame.display.flip()
            self.clock.tick(60)

    def main_game(self):
        """Main game loop."""
        running = True
        while running:
            self.screen.fill(BACKGROUND_COLOR)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Player input
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.paddle_left.move(-PADDLE_SPEED)
            if keys[pygame.K_s]:
                self.paddle_left.move(PADDLE_SPEED)
            if keys[pygame.K_UP]:
                self.paddle_right.move(-PADDLE_SPEED)
            if keys[pygame.K_DOWN]:
                self.paddle_right.move(PADDLE_SPEED)

            # Game updates
            score_left, score_right = self.ball.update(self.paddle_left, self.paddle_right)
            self.score_left += score_left
            self.score_right += score_right

            # Drawing
            self.ball.draw(self.screen)
            self.paddle_left.draw(self.screen)
            self.paddle_right.draw(self.screen)
            self.draw_scores()

            pygame.display.flip()
            self.clock.tick(60)

    def draw_scores(self):
        """Draw the scores above each paddle."""
        # Left score
        text_left = self.score_font.render(str(self.score_left), True, WHITE)
        left_pos = (self.paddle_left.centerx - text_left.get_width() // 2,
                    20)
        self.screen.blit(text_left, left_pos)

        # Right score
        text_right = self.score_font.render(str(self.score_right), True, WHITE)
        right_pos = (self.paddle_right.centerx - text_right.get_width() // 2,
                     20)
        self.screen.blit(text_right, right_pos)

    def quit(self):
        """Clean up and exit the game."""
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()