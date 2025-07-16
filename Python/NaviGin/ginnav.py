import sys
import os
import math


# Hide support prompt and initialize pygame
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame as pg
pg.init()

class Game:
    def __init__(self):
        # Screen initializations
        self.width, self.height = 1000, 600
        self.screen = pg.display.set_mode((self.width, self.height))
        self.start_bg, self.bg_color = (0, 0, 0), (30, 30, 30)
        self.clock = pg.time.Clock()
        self.fps = 60

        # Game state flags
        self.running = True
        self.on_start_credits = True
        self.on_menu = False
        self.on_start_cutscene = False
        self.on_level1 = False
        self.on_level2 = False
        self.on_level3 = False
        self.on_end_cutscence = False
        self.on_end_credits = False

    def run(self):
        while self.running:
            self.init_credits()
            self.menu()
            self.temporary_screen()
        self.game_exit()

    def game_exit(self):
        self.running = False
        pg.quit()
        sys.exit()

    def flip(self):
        pg.display.flip()
        self.clock.tick(self.fps)

    def scale_to_height(self, image, target_height):
        ratio = target_height / image.get_height()
        new_width = int(image.get_width() * ratio)
        return pg.transform.scale(image, (new_width, target_height))

    def reset_key_states(self):
        _ = pg.key.get_pressed()
        pg.event.clear(pg.KEYDOWN)
        pg.event.pump()

    def draw_button(self, button_surface, rect, is_hovered, hover_alpha):
        temp_surface = button_surface.copy()
        if is_hovered:
            temp_surface.fill((hover_alpha, hover_alpha, hover_alpha), special_flags=pg.BLEND_MULT)
        self.screen.blit(temp_surface, rect)

    def create_placeholder_button(self, text, color):
        surf = pg.Surface((200, 60), pg.SRCALPHA)
        pg.draw.rect(surf, color, (0, 0, 200, 60), border_radius=10)
        font = pg.font.SysFont('Arial', 30)
        text_surf = font.render(text, True, (255, 255, 255))
        surf.blit(text_surf, text_surf.get_rect(center=(100, 30)))
        return surf

    def create_placeholder_title(self):
        surf = pg.Surface((400, 150), pg.SRCALPHA)
        pg.draw.rect(surf, (100, 100, 255), (0, 0, 400, 150), border_radius=15)
        font = pg.font.SysFont('Arial', 50)
        text_surf = font.render("GAME TITLE", True, (255, 255, 255))
        surf.blit(text_surf, text_surf.get_rect(center=(200, 75)))
        return surf

    def handle_menu_events(self, selected_button):
        for event in pg.event.get():
            if event.type == pg.QUIT:
                self.game_exit()
            elif event.type == pg.KEYDOWN:
                match event.key:
                    case pg.K_ESCAPE | pg.K_BACKSPACE:
                        self.game_exit()
                    case pg.K_RETURN if selected_button in (0, 2):
                        self.on_menu = False
                        self.start_cutscene = True
                        return
                    case pg.K_RETURN if selected_button == 1:
                        self.game_exit()

    def init_credits(self):
        if not self.on_start_credits:
            return

        try:
            inuke_logo = pg.image.load('assets/inuke_logo.png').convert_alpha()
            dragon_logo = pg.image.load('assets/inuke_pfp4.png').convert_alpha()
        except:
            print("Logo files not found! Using placeholders")
            inuke_logo = pg.Surface((300, 150), pg.SRCALPHA)
            pg.draw.rect(inuke_logo, (255, 0, 0), (0, 0, 300, 150), 2)
            dragon_logo = pg.Surface((400, 200), pg.SRCALPHA)
            pg.draw.rect(dragon_logo, (0, 255, 0), (0, 0, 400, 200), 2)

        inuke_logo = self.scale_to_height(inuke_logo, 150)
        dragon_logo = self.scale_to_height(dragon_logo, 200)

        spacing = 0
        total_width = inuke_logo.get_width() + dragon_logo.get_width()
        inuke_pos = ((self.width - total_width - spacing) // 2, (self.height - 150) // 2)
        dragon_pos = (inuke_pos[0] + inuke_logo.get_width() + spacing, (self.height - 200) // 2)

        alpha_inuke = alpha_dragon = text_alpha = display_time = 0
        fade_speed = 2
        showing_both = False
        dragon_logo.set_alpha(alpha_dragon)

        ## ============================================================
        ##                  CREDIT PRESENTATION LOOP
        ## ============================================================
        while self.on_start_credits:
            self.screen.fill(self.start_bg)

            for event in pg.event.get():
                if event.type in (pg.QUIT, pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    self.on_start_credits = False
                    self.on_menu = True

            if not showing_both:
                if alpha_inuke < 255:
                    alpha_inuke = min(alpha_inuke + fade_speed, 255)
                    inuke_logo.set_alpha(alpha_inuke)
                elif alpha_dragon < 255:
                    alpha_dragon = min(alpha_dragon + fade_speed, 255)
                    dragon_logo.set_alpha(alpha_dragon)
                else:
                    showing_both = True

            if showing_both:
                display_time += 1
                if display_time >= 5 * self.fps:
                    self.on_start_credits = False
                    self.on_menu = True
                if alpha_inuke == 255 and alpha_dragon == 255:
                    text_alpha = min(text_alpha + 3, 255)

                text_surf = pg.font.SysFont('Consolas', 20).render("Presents . . .", True, (150, 150, 150))
                text_with_alpha = text_surf.copy()
                text_with_alpha.set_alpha(text_alpha)
                self.screen.blit(
                    text_with_alpha, 
                    text_with_alpha.get_rect(
                        center=(self.width // 2, 
                                self.height - 75
                            )
                    )
                )

            self.screen.blit(inuke_logo, inuke_pos)
            self.screen.blit(dragon_logo, dragon_pos)
            self.flip()

        self.reset_key_states()

    def menu(self):
        if not self.on_menu:
            return

        try:
            play_button = pg.image.load('assets/play_button.png').convert_alpha()
            exit_button = pg.image.load('assets/exit_button.png').convert_alpha()
            title_img = pg.image.load('assets/title.png').convert_alpha()
            bg_img = pg.image.load('assets/menu_bg.png').convert()
            bg_img = pg.transform.scale(bg_img, (self.width, self.height))

            # Create a darkened version of the background
            dark_bg = pg.Surface((self.width, self.height))
            dark_bg.fill((120, 120, 120))  # Dark overlay color (adjust values as needed)
            bg_img.blit(dark_bg, (0, 0), special_flags=pg.BLEND_MULT)
        except:
            print("Menu assets not found! Using placeholders")
            play_button = self.create_placeholder_button("PLAY", (0, 200, 0))
            exit_button = self.create_placeholder_button("EXIT", (200, 0, 0))
            title_img = self.create_placeholder_title()
            bg_img = pg.Surface((self.width, self.height))
            bg_img.fill((20, 20, 40))

        play_button = self.scale_to_height(play_button, 50)
        exit_button = self.scale_to_height(exit_button, 50)
        title_img = self.scale_to_height(title_img, 200)

        spacing = 80
        total_buttons_width = play_button.get_width() + exit_button.get_width() + spacing
        buttons_y = self.height // 2 + 100

        play_rect = pg.Rect(
            (self.width - total_buttons_width) // 2, 
            buttons_y, play_button.get_width(), 
            play_button.get_height()
        )
        exit_rect = pg.Rect(
            play_rect.right + spacing, 
            buttons_y, exit_button.get_width(), 
            exit_button.get_height()
        )

        title_base_y = self.height // 4
        time_accumulator = 0
        hover_alpha = 150
        selected_button = 2
        key_delay = 50

        ## ============================================================
        ##                        MENU LOOP
        ## ============================================================
        while self.on_menu:
            time_accumulator += 0.05
            title_y = title_base_y + math.sin(time_accumulator) * 15

            mouse_pos = pg.mouse.get_pos()
            mouse_clicked = pg.mouse.get_pressed()[0]
            keys = pg.key.get_pressed()

            self.handle_menu_events(selected_button)

            play_hovered = play_rect.collidepoint(mouse_pos)
            exit_hovered = exit_rect.collidepoint(mouse_pos)

            if key_delay <= 0:
                if keys[pg.K_LEFT] and selected_button != 0:
                    selected_button = 0
                    key_delay = 15
                elif keys[pg.K_RIGHT] and selected_button != 1:
                    selected_button = 1
                    key_delay = 15
                elif keys[pg.K_DOWN]:
                    selected_button = 2
                    key_delay = 15
            else:
                key_delay -= 1

            if mouse_clicked and (play_hovered or exit_hovered):
                if play_hovered or selected_button == 0 or selected_button == 2:
                    self.on_menu = False
                    self.start_cutscene = True
                    return
                elif exit_hovered or selected_button == 1:
                    self.game_exit()

            self.screen.blit(bg_img, (0, 0))
            self.screen.blit(title_img, ((self.width - title_img.get_width()) // 2, title_y))

            self.draw_button(play_button, play_rect, play_hovered or selected_button == 0, hover_alpha)
            self.draw_button(exit_button, exit_rect, exit_hovered or selected_button == 1, hover_alpha)

            self.flip()

    def temporary_screen(self):
        while True:
            self.screen.fill((0, 0, 0))
            text_surface = pg.font.SysFont('Consolas', 30, bold=True).render(
                "YOU ARE IN A TEMPORARY SCREEN, PRESS TO EXIT",
                True,
                (255, 0, 0)
            )
            self.screen.blit(text_surface, text_surface.get_rect(center=(self.width // 2, self.height // 2)))

            for event in pg.event.get():
                if event.type == pg.QUIT or event.type in (pg.KEYDOWN, pg.MOUSEBUTTONDOWN):
                    self.game_exit()

            self.flip()

    def start_cutscene(self):
        pass 

    def level1_main(self):
        pass 

    def level2_main(self):
        pass 

    def level3_main(self):
        pass 

    def end_cutscene(self):
        pass

    def end_credits(self):
        pass 


if __name__ == "__main__":
    Game().run()