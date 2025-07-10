import math
import os
import sys


# Pygame initialization
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame as pg
pg.init()
vec2 = pg.math.Vector2


class Game:
    """
    A comprehensive Pygame application framework with menu and game states.
    """

    def __init__(self, screen_size, fps = 60):
        """
        Initialize the game application.
        """
        self.screen_size = screen_size
        self.fps = fps
        self.bg_color = (20, 20, 30)  # Dark blue-gray
        
        # Pygame setup
        self.screen = pg.display.set_mode(self.screen_size)
        pg.display.set_caption("Pygame Application")
        self.clock = pg.time.Clock()
        self.font = pg.font.SysFont('Arial', 24)
        
        # Game states
        self.is_menu = True
        self.is_game = False
        self.running = True  # Main application running flag

    def run(self):
        """
        Main game loop controller.
        Handles the transition between menu and game states.
        """
        try:
            while self.running:
                if self.is_menu:
                    self.menu()
                elif self.is_game:
                    self.run_game()
        finally:
            pg.quit()
            sys.exit()

    def menu(self):
        """
        Handle the menu state rendering and input.
        Displays a simple menu and processes user input to transition to game state.
        """
        title_text = self.font.render("Pygame Application", True, (255, 255, 255))
        start_text = self.font.render("Press SPACE to start or ESC to quit", True, (200, 200, 200))
        
        while self.is_menu and self.running:
            self.screen.fill(self.bg_color)
            
            # Render menu text
            self.screen.blit(title_text, (self.screen_size[0]//2 - title_text.get_width()//2, 100))
            self.screen.blit(start_text, (self.screen_size[0]//2 - start_text.get_width()//2, 200))
            
            for event in pg.event.get():
                self.handle_events(event)
                
                if event.type == pg.KEYDOWN:
                    match event.key:
                        case pg.K_SPACE:
                            self.is_menu = False
                            self.is_game = True
                        case pg.K_ESCAPE:
                            self.is_menu = False
                            self.running = False
            
            pg.display.flip()
            self.clock.tick(self.fps)

    def run_game(self):
        """
        Main game loop handling events, updates, and rendering.
        """
        while self.is_game and self.running:
            # Process events
            for event in pg.event.get():
                self.handle_events(event)
            
            # Update game state
            self.update()
            
            # Render everything
            self.draw()
            
            # Maintain FPS
            self.clock.tick(self.fps)

    def update(self):
        """
        Update game state. 
        """
        pass

    def handle_events(self, event):
        """
        Handle common events for both menu and game states.
        """
        if event.type == pg.QUIT:
            self.running = False
            self.is_game = False
        elif event.type == pg.KEYDOWN:
            self.handle_keyboard_events(event)
        elif event.type in (pg.MOUSEBUTTONDOWN, pg.MOUSEBUTTONUP): #, pg.MOUSEMOTION):
            self.handle_mouse_events(event)

    def handle_keyboard_events(self, event):
        """
        Handle keyboard input events.

        Args:
            event: Pygame keyboard event
        """
        match event.key:
            case pg.K_ESCAPE:
                self.is_game = False
                self.is_menu = True
            case _:
                pass  # Add game-specific key handling

    def handle_mouse_events(self, event):
        """
        Handle mouse input events.
        """
        mouse_pos = vec2(pg.mouse.get_pos())
        
        if event.type == pg.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                pass  # Add left click handling
            elif event.button == 3:  # Right click
                pass  # Add right click handling

    def draw(self):
        """
        Render all game elements.
        """
        self.screen.fill(self.bg_color)
        
        # Add game-specific drawing here
        
        pg.display.flip()


if __name__ == "__main__":
    game = Game()
    game.run()