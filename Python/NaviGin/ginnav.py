import sys
import random
import math
import matplotlib
import os
from collections import defaultdict

import pygame as pg
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
pg.init()

class Game:
    def __init__(self):
        self.width = 1000
        self.height = 600 
        self.screen = pg.display.set_mode((self.width, self.height))
        self.start_bg = (0,0,0)
        self.bg_color = (30,30,30)
        self.clock = pg.time.Clock()
        self.fps = 60

        self.running = True 
        self.on_start_credits = True 
        self.on_menu = False 
        self.on_start_cutscene = False 
        self.on_level1 = False
        self.on_level2 = False 
        self.on_level3 = False
        self.on_end_cutscence = False 
        self.on_end_credits = False 

    def scale_to_height(self, image, target_height):
        """Helper function to scale image while maintaining aspect ratio"""
        ratio = target_height / image.get_height()
        new_width = int(image.get_width() * ratio)
        return pg.transform.scale(image, (new_width, target_height))

    def flip(self):
        pg.display.flip()
        self.clock.tick(self.fps)

    def game_exit(self):
        self.running = False
        pg.quit()
        sys.exit()

    def run(self):
        while self.running:
            self.init_credits()
            self.menu()
            self.temporary_screen()
        self.game_exit()

    def init_credits(self):
        if not self.on_start_credits:
            return
        
        # Load your logo assets
        try:
            inuke_logo = pg.image.load('assets/inuke_logo.png').convert_alpha()
            dragon_logo = pg.image.load('assets/inuke_pfp4.png').convert_alpha()
        except:
            # Fallback if files not found - replace with your actual paths
            print("Logo files not found! Using placeholders")
            inuke_logo = pg.Surface((300, 150), pg.SRCALPHA)
            pg.draw.rect(inuke_logo, (255, 0, 0), (0, 0, 300, 150), 2)
            dragon_logo = pg.Surface((400, 200), pg.SRCALPHA)
            pg.draw.rect(dragon_logo, (0, 255, 0), (0, 0, 400, 200), 2)
        
        inuke_height = 150
        dragon_height = 200
        inuke_logo = self.scale_to_height(inuke_logo, inuke_height)
        dragon_logo = self.scale_to_height(dragon_logo, dragon_height)
        
        # Calculate positions for side-by-side display
        total_width = inuke_logo.get_width() + dragon_logo.get_width()
        spacing = 0  # Space between logos
        
        inuke_pos = (
            (self.width - total_width - spacing) // 2,
            (self.height - inuke_height) // 2
        )
        dragon_pos = (
            inuke_pos[0] + inuke_logo.get_width() + spacing,
            (self.height - dragon_height) // 2
        )

        # Animation variables
        alpha_inuke = 0
        alpha_dragon = 0
        text_alpha = 0 
        display_time = 0
        fade_speed = 2  # How fast the fade in happens
        showing_both = False
        dragon_logo.set_alpha(alpha_dragon)

        
        ## ======================================
        ##       CREDIT PRESENTATION LOOP
        ## ======================================
        while self.on_start_credits:
            self.screen.fill(self.start_bg)
            
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.running = False
                    pg.quit()
                    sys.exit()
                if event.type == pg.KEYDOWN or event.type == pg.MOUSEBUTTONDOWN:
                    # Skip animation if player presses any key or clicks
                    self.on_start_credits = False
                    self.on_menu = True
                    
            
            # Handle logo fade-in sequence
            if not showing_both:
                # First fade in Inuke logo
                if alpha_inuke < 255:
                    alpha_inuke = min(alpha_inuke + fade_speed, 255)
                    inuke_logo.set_alpha(alpha_inuke)
                    
                
                # Then fade in game logo after Inuke is fully visible
                elif alpha_dragon < 255:
                    alpha_dragon = min(alpha_dragon + fade_speed, 255)
                    dragon_logo.set_alpha(alpha_dragon)
                # Both logos are fully visible
                else:
                    showing_both = True
            
            # Count how long both logos have been displayed
            if showing_both:
                display_time += 1
                if display_time >= 5 * self.fps:  # 5 seconds at 60 FPS
                    self.on_start_credits = False
                    self.on_menu = True
                # Only start fading in text after both logos are fully visible
                if alpha_inuke == 255 and alpha_dragon == 255:
                    text_alpha = min(text_alpha + 3, 255)  # Increase alpha gradually
                
                # Create a surface for the text with per-pixel alpha
                text_surface = pg.font.SysFont('Consolas', 20).render(
                    "Presents . . .", 
                    True, 
                    (150, 150, 150)
                )
                
                # Create a copy of the surface to apply alpha to
                text_with_alpha = text_surface.copy()
                text_with_alpha.set_alpha(text_alpha)  # Apply the current alpha
                
                # Position and blit the text
                text_rect = text_with_alpha.get_rect(center=(self.width//2, self.height - 75))
                self.screen.blit(text_with_alpha, text_rect)
            
            # Draw logos with current alpha values
            self.screen.blit(inuke_logo, inuke_pos)
            self.screen.blit(dragon_logo, dragon_pos)
            
            self.flip()
        
        self.reset_key_states()

    def menu(self):
        if not self.on_menu:
            return
        # Load assets
        try:
            play_button = pg.image.load('assets/play_button.png').convert_alpha()
            exit_button = pg.image.load('assets/exit_button.png').convert_alpha()
            title_img = pg.image.load('assets/title.png').convert_alpha()
            bg_img = pg.image.load('assets/menu_bg.png').convert()
            bg_img = pg.transform.scale(bg_img, (self.width, self.height))
        except:
            # Fallback if files not found
            print("Menu assets not found! Using placeholders")
            play_button = self.create_placeholder_button("PLAY", (0, 200, 0))
            exit_button = self.create_placeholder_button("EXIT", (200, 0, 0))
            title_img = self.create_placeholder_title()
            bg_img = pg.Surface((self.width, self.height))
            bg_img.fill((20, 20, 40))  # Dark blue background
        
        # Scale elements
        button_height = 50 
        title_height = 200 
        play_button = self.scale_to_height(play_button, button_height)
        exit_button = self.scale_to_height(exit_button, button_height)
        title_img = self.scale_to_height(title_img, title_height)
        
        # Calculate positions
        spacing = 80  # Space between buttons
        total_buttons_width = play_button.get_width() + exit_button.get_width() + spacing
        buttons_y = self.height // 2 + 100  # Position below center
        
        # Button rectangles for hover detection
        play_rect = pg.Rect(
            (self.width - total_buttons_width) // 2,
            buttons_y,
            play_button.get_width(),
            play_button.get_height()
        )
        exit_rect = pg.Rect(
            play_rect.right + spacing,
            buttons_y,
            exit_button.get_width(),
            exit_button.get_height()
        )
        
         # Animation variables
        title_base_y = self.height // 4  # Base Y position for title
        time_accumulator = 0
        hover_alpha = 180  # Alpha when button is hovered (out of 255)
        selected_button = 2  # 2 = nothing selected, 0 = play, 1 = exit
        key_delay = 50  # For preventing rapid key repeats
        
        ## ===============================
        ##          MENU LOOP
        ## ===============================
        while self.on_menu:
            # Calculate animation values
            time_accumulator += 0.05
            title_y = title_base_y + math.sin(time_accumulator) * 15  # Sinusoidal movement
            
            # Get input states
            mouse_pos = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()[0]
            keys = pg.key.get_pressed()
            
            # Handle events
            self.handle_menu_events(selected_button)
            
            # Check for button hover
            play_hovered = play_rect.collidepoint(mouse_pos)
            exit_hovered = exit_rect.collidepoint(mouse_pos)
            
            # Keyboard navigation with delay to prevent rapid toggling
            if key_delay <= 0:
                if keys[pg.K_LEFT] and selected_button != 0:
                    selected_button = 0  # Select play button
                    key_delay = 15
                elif keys[pg.K_RIGHT] and selected_button != 1:
                    selected_button = 1  # Select exit button
                    key_delay = 15
                elif keys[pg.K_DOWN]:
                    selected_button = 2  # Deselect both
                    key_delay = 15
            else:
                key_delay -= 1
            
            # Handle selection (mouse or keyboard)
            
            
            # Handle selection (mouse or keyboard)
            if (mouse_clicked and (play_hovered or exit_hovered)):
                if play_hovered or selected_button == 0 or selected_button == 2:
                    # If play is hovered, selected (0), or nothing is selected (2)
                    self.on_menu = False
                    self.start_cutscene = True
                    return
                elif exit_hovered or selected_button == 1:
                    # Only exit if explicitly selected (1) or hovered
                    self.game_exit()
            
            # Draw everything
            self.screen.blit(bg_img, (0, 0))
            
            # Draw title with sinusoidal movement
            title_pos = (
                (self.width - title_img.get_width()) // 2,
                title_y
            )
            self.screen.blit(title_img, title_pos)
            
            # Draw buttons with hover effects
            self.draw_button(play_button, play_rect, 
                        play_hovered or selected_button == 0, 
                        hover_alpha)
            self.draw_button(exit_button, exit_rect, 
                            exit_hovered or selected_button == 1, 
                            hover_alpha)
            
            self.flip()

    def draw_button(self, button_surface, rect, is_hovered, hover_alpha):
        """Draw a button with hover effect"""
        temp_surface = button_surface.copy()
        if is_hovered:
            # Darken the button by reducing alpha
            temp_surface.fill((hover_alpha, hover_alpha, hover_alpha), special_flags=pg.BLEND_MULT)
        self.screen.blit(temp_surface, rect)

    def create_placeholder_button(self, text, color):
        """Create a placeholder button if image not found"""
        surf = pg.Surface((200, 60), pg.SRCALPHA)
        pg.draw.rect(surf, color, (0, 0, 200, 60), border_radius=10)
        font = pg.font.SysFont('Arial', 30)
        text_surf = font.render(text, True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(100, 30))
        surf.blit(text_surf, text_rect)
        return surf

    def create_placeholder_title(self):
        """Create a placeholder title if image not found"""
        surf = pg.Surface((400, 150), pg.SRCALPHA)
        pg.draw.rect(surf, (100, 100, 255), (0, 0, 400, 150), border_radius=15)
        font = pg.font.SysFont('Arial', 50)
        text_surf = font.render("GAME TITLE", True, (255, 255, 255))
        text_rect = text_surf.get_rect(center=(200, 75))
        surf.blit(text_surf, text_rect)
        return surf

    def handle_menu_events(self, selected_button):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.running = False
                pg.quit()
                sys.exit()
            if event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE | pg.K_BACKSPACE:  # Combined cases for same action
                        self.game_exit()
                    case pg.K_RETURN if selected_button in (0, 2):  # With condition
                        self.on_menu = False
                        self.start_cutscene = True
                        return
                    case pg.K_RETURN if selected_button == 1:  # Alternative RETURN case
                        self.game_exit()
                    case pg.K_LEFT:
                        selected_button = max(0, selected_button - 1)  # Example for left arrow
                    case pg.K_RIGHT:
                        selected_button = min(1, selected_button + 1)  # Example for right arrow
                    case _:  # Default case (optional)
                        pass  # Handle other keys or do nothing



    def temporary_screen(self):
        """Display a temporary screen that exits on any key press or mouse click"""
        while True:
            self.screen.fill((0, 0, 0))
            
            # Render the text
            text_surface = pg.font.SysFont('Consolas', 30, bold = True).render(
                "YOU ARE IN A TEMPORARY SCREEN, PRESS TO EXIT", 
                True, 
                (255, 0,0)   
            )
            
            # Position and display the text
            text_rect = text_surface.get_rect(center=(self.width//2, self.height//2))
            self.screen.blit(text_surface, text_rect)
            
            # Check for any input event
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    self.game_exit()
                elif event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    # Exit on any key press or mouse click
                    self.game_exit()
            
            # Update the display
            pg.display.flip()
            self.clock.tick(self.fps)
    
    def reset_key_states(self):
        """Force-reset all keyboard states by getting fresh input events"""
        # Get all current key states to clear the buffer
        _ = pg.key.get_pressed()
        # Clear the event queue of all KEYDOWN events
        pg.event.clear(pg.KEYDOWN)
        # Pump the event queue to ensure fresh state
        pg.event.pump()






# Create and run simulation
if __name__ == "__main__":
    game = Game()
    game.run()



