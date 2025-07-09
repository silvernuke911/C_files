import sys
import random
import math
import matplotlib
import os
from collections import defaultdict

# Pygame initialization
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"
import pygame
pygame.init()

def resource_path(relative_path):
    """ Get absolute path to resource (for dev and PyInstaller). """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)
icon = pygame.image.load(resource_path("partikol 2.0 icon.png"))
pygame.display.set_icon(icon)

class Button:
    def __init__(self, dimension, position, text, 
                font_name, font_size, 
                bg_color, text_color, 
                hover_color, border_color = (200,200,200)):
        self.w, self.h = dimension 
        self.x0, self.y0 = position  
        self.rect = pygame.Rect(self.x0, self.y0, self.w, self.h) 
        self.text = text
        self.font = pygame.font.SysFont(font_name, font_size)
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.hover_color = hover_color
        self.hovered = False

    def draw(self, surface: pygame.Surface):
        color = self.hover_color if self.hovered else self.bg_color
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, self.border_color, self.rect, 3)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def update(self, mouse_pos):
        self.hovered = self.rect.collidepoint(mouse_pos)

    def is_clicked(self, event: pygame.event.Event) -> bool:
        return (self.hovered and 
                event.type == pygame.MOUSEBUTTONDOWN and 
                event.button == 1)

class Simulation:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.fullscreen = False
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Partikol 2.0")
        
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Consolas", 16)
        self.small_font = pygame.font.SysFont("Consolas", 12)
        
        self.particles = []
        self.particle_count = []
        self.energy_history = []
        self.temperature_history = []
        self.most_max_speed = 1.0
        
        # Simulation parameters
        self.gravity = False
        self.damping = False
        self.evaporation = False
        self.collision_damping = False
        self.damping_factor = 0.9
        self.collision_damping_factor = 0.95
        self.time_scale = 1
        self.time_step = 2
        self.draw_plots = True
        self.running = False
        self.is_menu = True
        self.bin_gap = 2.5
        self.bin_gap_overide = False
        self.particle_radius = 10
        self.time = 0
        self.show_ui = True
        self.cell_size = 50
        self.max_history = 200
        self.fps = 60
        self.f_key_pressed = False   ## for rapid firing
        self.last_particle_time = 0
        self.particle_spawn_interval = 100  # milliseconds (0.25 seconds)
        self.show_cell_density = False
        self.cell_density = {}
        self.inferno_cmap = matplotlib.colormaps.get_cmap('inferno')
        self.show_help = False
        self.help_font = pygame.font.SysFont("Consolas", 12)
        self.help_text = [
            "---------------------------------------------------",
            "                PARTIKOL 2.0 CONTROLS              ",
            "---------------------------------------------------",
            "LEFT CLICK  : Create & drag particle",
            "RIGHT CLICK : Repel particles",
            "F           : Hold to continuously create particles",
            "A           : Select particle under cursor",
            "X           : Clear all particles",
            "B           : Repel particles",
            "R           : Add 100 random particles",
            "C           : Add cluster of particles around mouse",
            "G           : Toggle gravity",
            "D           : Toggle damping",
            "C           : Toggle particle collision damping",
            "Z           : Increase particle energy",
            "0           : Stop all particles",
            "SPACE       : Pause simulation",
            "F1          : Toggle UI",
            "F2          : Show/hide this help",
            "F11         : Toggle fullscreen",
            "ARROWS L/R  : Navigate particle trajectory",
            "ARROWS D    : Exit particle trajectory",
            "+/-         : Change particle size",
            "1           : Default velocity bin sizes",
            "2-4         : Change velocity bin sizes",
            "6           : Toggle density visualization",
            "7           : Clear trajectories",
            "9           : Toggle evaporation",
            "BACKSPACE   : Return to menu",
            "DELETE      : Exit"
        ]

        
        # Interaction state
        self.selected_index = -1
        self.current_particle = None
        self.dragging = False
        self.dragging_with_key = False
        self.f_pressed = False
        self.paused = False
    
    def run(self):
        while True: 
            if self.is_menu:
                self.menu()
            else:
                self.run_simulation()

    def menu(self):

        def sim_restart():
            self.show_ui = True 
            self.time = 0
            self.particle_radius = 10
            self.particles = []
            self.particle_count = []
            self.energy_history = []
            self.temperature_history = []
            self.gravity = False 
            self.evaporation = False 
            self.damping = False 
            self.collision_damping = False 
            play_button.hovered = True
            self.running = True
            self.is_menu = False
            
        # Font setup
        title_font = pygame.font.SysFont("Consolas", 40, bold=True)
        credit_font = pygame.font.SysFont("Consolas", 15)
        
        # Button setup
        play_button_w, play_button_h = 200, 40
        play_button = Button(
            (play_button_w, play_button_h),
            (self.width / 2 - play_button_w / 2, 330), 
            "Run", "Consolas", 18, 
            (30, 30, 30), (255, 255, 255), (60, 60, 60)
        )
        play_button.hover_color = (0,0,0)

        # Menu container dimensions
        menu_width = 500
        menu_height = 250
        menu_rect = pygame.Rect(
            self.width // 2 - menu_width // 2,
            self.height // 2 - menu_height // 2,
            menu_width,
            menu_height
        )
        
        trippy_effect = False
        if random.randint(0,4) == 0:
            self.gravity = True
        else: self.gravity = False 

        self.is_menu = True
        self.show_ui = False
        self.particles = []
        self.particle_radius = 7.5
        self.add_random_particles(150)
        for p in self.particles:
            p.vel = pygame.Vector2(random.uniform(-5, 5), random.uniform(-5, 5))

        while self.is_menu:
            if not trippy_effect:
                # Clear screen once per frame
                self.screen.fill((10, 10, 10))
            
            # Update and draw simulation first (background)
            self.update()
            self.draw()
            
            mouse_pos = pygame.mouse.get_pos()
            is_hovered = menu_rect.collidepoint(mouse_pos)

            # Draw menu container (before UI elements)
            inner_color = (20, 0, 0) if is_hovered else (0, 0, 0)
            pygame.draw.rect(self.screen, inner_color, menu_rect.inflate(-4, -4))
            pygame.draw.rect(self.screen, (200, 0, 0), menu_rect, 5)
            
            # Draw all UI elements (on top of container)
            title = title_font.render("PARTICLE SIMULATION", True, (255, 255, 255))
            self.screen.blit(title, (menu_rect.centerx - title.get_width() // 2, menu_rect.y + 30))
            
            credits = credit_font.render("cc. V. Juan", True, (230, 230, 230))
            self.screen.blit(credits, (menu_rect.centerx - credits.get_width() // 2, menu_rect.y + 80))
            
            instructions = credit_font.render("Press F2 in simulation to access instructions", True, (200, 200, 200))
            self.screen.blit(instructions, (menu_rect.centerx - instructions.get_width() // 2, menu_rect.y + 120))
            
            # Handle button last (on top of everything)
            play_button.update(mouse_pos)
            play_button.draw(self.screen)
            
            # Event handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if play_button.is_clicked(event):
                    sim_restart()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER or event.key == pygame.K_SPACE:
                        sim_restart()
                        
                    if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                        self.is_menu = False
                        self.running = False
                        pygame.quit()
                        sys.exit()
                    
                    if event.key == pygame.K_g:  # Toggle gravity
                        self.gravity = not self.gravity
                        self.evaporation = False
                    
                    if event.key == pygame.K_d:  # Toggle damping
                        self.damping = not self.damping

                    if event.key == pygame.K_z:  # Increase the kinetic energy of all particles
                        for p in self.particles:
                            if p.vel == pygame.math.Vector2(0,0):
                                p.vel = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))
                            else: p.vel *= math.sqrt(1.2)
                    
                    if event.key == pygame.K_8 or event.key == pygame.K_KP_8:  # Toggle collision damping
                        self.collision_damping = not self.collision_damping

                    elif event.key == pygame.K_6:  # Toggle cell density visualization
                        self.show_cell_density = not self.show_cell_density
                        if self.show_cell_density:
                            self.calculate_cell_density()

                    
                
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    trippy_effect = True
                
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    trippy_effect = False

            pygame.display.flip()
            self.clock.tick(60)

    def run_simulation(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(self.fps)
    
    def system_reset(self):
        self.selected_index = -1
        self.current_particle = None
        self.dragging = False
        self.dragging_with_key = False
        self.f_pressed = False
        self.paused = False
        self.particles = []
        self.particle_count = []
        self.energy_history = []
        self.temperature_history = []
        self.most_max_speed = 1.0
        
        # Simulation parameters
        self.gravity = False
        self.damping = False
        self.evaporation = False
        self.collision_damping = False
        self.damping_factor = 0.9
        self.collision_damping_factor = 0.95
        self.time_scale = 1
        self.time_step = 2
        self.draw_plots = True
        self.running = False
        self.is_menu = True
        self.bin_gap = 2.5
        self.bin_gap_overide = False
        self.particle_radius = 10
        self.time = 0
        self.show_ui = True
        self.cell_size = 50
        self.max_history = 200
        self.fps = 60
        self.f_key_pressed = False   ## for rapid firing
        self.last_particle_time = 0
        self.show_cell_density = False
        self.cell_density = {}
        self.show_help = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                pygame.quit()
                sys.exit()

            self.handle_keyboard_events(event)
            self.handle_mouse_events(event)
            self.handle_long_presses()
    
    def handle_long_presses(self):
        current_time = pygame.time.get_ticks()
        keys = pygame.key.get_pressed()
        
        # if not any(p.dragging for p in self.particles):
        if keys[pygame.K_f]:
            if not self.f_key_pressed:  # Initial press
                self.f_key_pressed = True
                self.last_particle_time = current_time
                self.create_particle_at_mouse()
            
            # Continuous creation while held
            elif current_time - self.last_particle_time > self.particle_spawn_interval:
                self.last_particle_time = current_time
                self.create_particle_at_mouse()
        else:
            self.f_key_pressed = False

    def handle_keyboard_events(self, event):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.system_reset()
                self.running = False
                self.is_menu = True

            elif event.key == pygame.K_F2:  # Toggle help
                self.show_help = not self.show_help

            if event.key == pygame.K_a:
                if self.selected_index != -1:
                    self.selected_index = -1
                else:
                    self.selected_index = -1  # Reset selection first
                    for i, particle in enumerate(reversed(self.particles)):  # Check front-to-back
                        if (particle.pos - mouse_pos).length() <= particle.radius:
                            self.selected_index = len(self.particles) - 1 - i  # Convert reverse index
                            break
 
            if event.key == pygame.K_x:  # Clear all particles
                self.time = 0
                self.particles = []
                self.selected_index = -1
                self.time_scale = 1
                self.most_max_speed = 1.0
                self.particle_count = []
                self.energy_history = []               
                self.temperature_history = []

            elif event.key == pygame.K_DELETE:
                self.running = False
                self.gravity = False 
                self.damping = False 
                self.collision_damping = False
                pygame.quit()
                sys.exit()

            if event.key == pygame.K_v:
                self.most_max_speed = 1

            elif event.key == pygame.K_r:  # Random particles
                self.add_random_particles(100)
            
            elif event.key == pygame.K_c:  # Cluster around mouse
                self.add_cluster_around_mouse(100)
            
            elif event.key == pygame.K_g:  # Toggle gravity
                self.gravity = not self.gravity
                self.evaporation = False
            
            elif event.key == pygame.K_d:  # Toggle damping
                self.damping = not self.damping
            
            elif event.key == pygame.K_LEFT and self.particles:  # Select previous particle
                self.selected_index = (self.selected_index - 1) % len(self.particles)
            
            elif event.key == pygame.K_RIGHT and self.particles:  # Select next particle
                self.selected_index = (self.selected_index + 1) % len(self.particles)
            
            elif event.key == pygame.K_DOWN:  # Deselect particle
                self.selected_index = -1
            
            elif event.key == pygame.K_COMMA:  # Decrease time scale
                self.time_scale /= self.time_step
            
            elif event.key == pygame.K_PERIOD:  # Increase time scale
                self.time_scale *= self.time_step
            
            elif event.key == pygame.K_SLASH:  #  Return time scale to 1
                self.time_scale = 1

            elif event.key == pygame.K_f:  # Create particle with F key
                self.f_pressed = True
                mx, my = pygame.mouse.get_pos()
                p = Particle(mx, my, radius=self.particle_radius)
                p.dragging = True
                self.current_particle = p
                self.dragging = True
                self.dragging_with_key = True
                self.particles.append(p)

            if event.key == pygame.K_SPACE:  # Toggle pause
                self.paused = not self.paused

            if event.key == pygame.K_e:  # Remove particles near mouse
                self.remove_particles_near_mouse()
            
            if event.key == pygame.K_b:  # Force particles to move
                self.bomb_force()

            if event.key == pygame.K_z:  # Increase the kinetic energy of all particles
                for p in self.particles:
                    if p.vel == pygame.math.Vector2(0,0):
                        p.vel = pygame.math.Vector2(random.uniform(-1,1), random.uniform(-1,1))
                    else: p.vel *= math.sqrt(1.2)

            elif event.key == pygame.K_1 or event.key == pygame.K_KP_1:  ## velocity graph bin gap
                self.bin_gap_overide = False
                self.most_max_speed = 1
                
            elif event.key == pygame.K_2 or event.key == pygame.K_KP_2: 
                self.bin_gap_overide = True 
                self.most_max_speed = 1
                self.bin_gap = 0.5
            elif event.key == pygame.K_3 or event.key == pygame.K_KP_3:  
                self.bin_gap_overide = True 
                self.most_max_speed = 1
                self.bin_gap = 2.5
            elif event.key == pygame.K_4 or event.key == pygame.K_KP_4:  
                self.bin_gap_overide = True 
                self.most_max_speed = 1
                self.bin_gap = 5

            elif event.key == pygame.K_0 or event.key == pygame.K_KP_0:
                for p in self.particles:
                    p.vel = pygame.math.Vector2(0,0)

            elif event.key == pygame.K_6:  # Toggle cell density visualization
                self.show_cell_density = not self.show_cell_density
                if self.show_cell_density:
                    self.calculate_cell_density()

            elif event.key == pygame.K_7 or event.key == pygame.K_KP_7:  # Toggle collision damping
                for p in self.particles:
                    p.trajectory = []

            elif event.key == pygame.K_8 or event.key == pygame.K_KP_8:  # Toggle collision damping
                self.collision_damping = not self.collision_damping

            elif event.key == pygame.K_9 or event.key == pygame.K_KP_9: # toggle evaporation
                if self.gravity:
                    self.evaporation = not self.evaporation
            
            if event.key == pygame.K_F1:
                self.show_ui = not self.show_ui

            elif event.key == pygame.K_F11:  # F11 to toggle
                self.toggle_fullscreen()

            elif event.key == pygame.K_EQUALS or event.key == pygame.K_KP_PLUS:  ## particle size
                temp_size = min(40,self.particle_radius*2 )
                self.particle_radius = temp_size
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:  
                temp_size = max(2.5,self.particle_radius/2 )
                self.particle_radius = temp_size

            
        
        if event.type == pygame.KEYUP and event.key == pygame.K_f and self.current_particle and self.dragging_with_key:
            mx, my = pygame.mouse.get_pos()
            drag_vector = self.current_particle.pos - pygame.Vector2(mx, my)
            self.current_particle.vel = drag_vector * 0.1
            self.current_particle.dragging = False
            self.current_particle = None
            self.dragging = False
            self.dragging_with_key = False
            self.f_pressed = False

    def update(self):
        if self.paused:
            return
        
        self.time += (1/self.fps) * self.time_scale

        if self.evaporation and self.gravity:
            self.particles = [
                p for p in self.particles 
                if not self.is_evaporating(p)
            ]
            # Reset selection if needed
            if self.selected_index >= len(self.particles):
                self.selected_index = -1

        # Update particles
        for p in self.particles:
            if not p.dragging:
                if self.gravity:
                    p.apply_force(pygame.Vector2(0, 0.2))  # gravity
                else:
                    p.apply_force(pygame.Vector2(0, 0))
            
            p.update()
            p.color = p.original_color
            p.check_bounds(self.width, self.height, self.damping, self.damping_factor)
        
        self.handle_collision()
        
        # Calculate energy and speeds
        kinetic_energy = 0
        temperature = 0
        speeds = []
        for p in self.particles:
            v = p.vel.length()
            speeds.append(v)
            kinetic_energy += 0.5 * p.mass * v**2
            temperature = kinetic_energy / len(self.particles)
        
        if self.show_cell_density:
            self.calculate_cell_density()

        self.energy_history.append(kinetic_energy)
        self.temperature_history.append(temperature)
        self.particle_count.append(len(self.particles))

        if len(self.energy_history) > self.max_history:
            self.energy_history.pop(0)
            self.temperature_history.pop(0)
            self.particle_count.pop(0)
        
    def handle_collision(self):
        # Spatial hashing for collision detection
        spatial_hash = defaultdict(list)
        for p in self.particles:
            cell = self.get_cell(p.pos)
            spatial_hash[cell].append(p)
        
        neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                            (0, -1), (0, 0), (0, 1),
                            (1, -1), (1, 0), (1, 1)]
        
        # Collision detection and response
        for p1 in self.particles:
            cell_x, cell_y = self.get_cell(p1.pos)
            for dx, dy in neighbor_offsets:
                neighbor_cell = (cell_x + dx, cell_y + dy)
                for p2 in spatial_hash.get(neighbor_cell, []):
                    if p1 is p2 or p1.dragging or p2.dragging:
                        continue
                    
                    delta = p1.pos - p2.pos
                    dist = delta.length()
                    combined_radius = p1.radius + p2.radius
                    
                    if 0 < dist < combined_radius:
                        direction = delta.normalize()
                        overlap = combined_radius - dist
                        p1.pos += direction * (overlap / 2)
                        p2.pos -= direction * (overlap / 2)
                        
                        # Realistic velocity transfer
                        normal = direction
                        tangent = pygame.Vector2(-normal.y, normal.x)
                        
                        v1n = normal.dot(p1.vel)
                        v1t = tangent.dot(p1.vel)
                        v2n = normal.dot(p2.vel)
                        v2t = tangent.dot(p2.vel)
                        
                        v1n_after = v2n
                        v2n_after = v1n

                        v1_final = v1n_after * normal + v1t * tangent
                        v2_final = v2n_after * normal + v2t * tangent
                        if not self.collision_damping:
                            p1.vel = v1_final
                            p2.vel = v2_final
                        else:
                            p1.vel = v1_final * self.collision_damping_factor
                            p2.vel = v2_final * self.collision_damping_factor
    
    def toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        
        if self.fullscreen:
            # Store current windowed size before going fullscreen
            if not hasattr(self, 'windowed_size'):
                self.windowed_size = (self.width, self.height)
            
            # Switch to fullscreen
            info = pygame.display.Info()
            self.screen = pygame.display.set_mode(
                (info.current_w, info.current_h), 
                pygame.FULLSCREEN
            )
            self.width, self.height = info.current_w, info.current_h
        else:
            # Restore windowed size
            self.screen = pygame.display.set_mode(self.windowed_size)
            self.width, self.height = self.windowed_size

    def bomb_force(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        for p in self.particles:
            direction = p.pos - mouse_pos
            distance = direction.length()
            if distance < 50 and distance > 0:
                force_magnitude = 50  # inverse-distance repulsion
                repulsive_force = direction.normalize() * force_magnitude
                p.apply_force(repulsive_force)

    def create_particle_at_mouse(self):
        mx, my = pygame.mouse.get_pos()
        new_particle = Particle(mx, my, radius=self.particle_radius)
        self.particles.append(new_particle)

    def remove_particles_near_mouse(self):
        mouse_pos = pygame.Vector2(pygame.mouse.get_pos())
        # Create a new list excluding particles within 100px of mouse
        self.particles = [
            p for p in self.particles 
            if (p.pos - mouse_pos).length() >= 100
        ]
        # Reset selection if the selected particle was removed
        if self.selected_index >= len(self.particles):
            self.selected_index = -1

    def handle_mouse_events(self, event):
        mouse_pos = pygame.mouse.get_pos()
        
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            p = Particle(*event.pos, radius=self.particle_radius)
            p.dragging = True
            self.current_particle = p
            self.dragging = True
            self.particles.append(p)
        
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.current_particle:
            drag_vector = self.current_particle.pos - pygame.Vector2(event.pos)
            self.current_particle.vel = drag_vector * 0.1
            self.current_particle.dragging = False
            self.current_particle = None
            self.dragging = False
        
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.Vector2(event.pos)
            for p in self.particles:
                direction = p.pos - mouse_pos
                distance = direction.length()
                if distance < 50 and distance > 0:
                    force_magnitude = 50  # inverse-distance repulsion
                    repulsive_force = direction.normalize() * force_magnitude
                    p.apply_force(repulsive_force)
    
    def add_random_particles(self, count):
        new_particles = []
        for _ in range(count):
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            p = Particle(x, y, radius=self.particle_radius)
            new_particles.append(p)
        self.particles.extend(new_particles)
    
    def add_cluster_around_mouse(self, count):
        mx, my = pygame.mouse.get_pos()
        particles_added = 0
        attempts = 0
        max_attempts = 400
        
        while particles_added < count and attempts < max_attempts:
            attempts += 1
            x = random.randint(mx - 100, mx + 100)
            y = random.randint(my - 100, my + 100)
            
            if (mx - x)**2 + (my - y)**2 < 100**2:
                x = max(0, min(x, self.width))
                y = max(0, min(y, self.height))
                p = Particle(x, y, radius=self.particle_radius)
                self.particles.append(p)
                particles_added += 1
    
    def is_evaporating(self, particle):
        """Check if particle should evaporate (touching top wall)"""
        return particle.pos.y - particle.radius <= 0
    
    def draw(self):
        if not self.is_menu:
            self.screen.fill((10, 10, 10))  # Dark gray background
        
        if self.show_cell_density:
            self.draw_cell_density()

        # Draw particles
        for p in self.particles:
            p.draw(self.screen)

        # Draw trajectory 
        if 0 <= self.selected_index < len(self.particles):
            p = self.particles[self.selected_index]
            skip = 1
            pygame.draw.circle(
                    self.screen, 
                    (255, 255, 255),  # White border color
                    (int(p.pos.x), int(p.pos.y)), 
                    p.radius + 3,  # Slightly larger than particle
                    min(3,p.radius * 0.3)  # Border thickness
                )
            if len(p.trajectory) > 4:
                pygame.draw.lines(self.screen, (255, 255, 255), False, p.trajectory[::skip], 2)
            p.draw(self.screen)

        # Draw drag line if dragging
        if self.dragging and self.current_particle:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(self.screen, (255, 0, 0), self.current_particle.pos, mouse_pos, 2)
            pygame.draw.circle(self.screen, (0, 200, 200), mouse_pos, 2)
        
        if self.show_ui:
            # Draw UI text
            self.draw_ui()
            
            # Draw plots if enabled
            if self.draw_plots:
                speeds = [p.vel.length() for p in self.particles]
                # self.draw_energy_plot(self.energy_history, (10, 40), (200, 80))
                self.draw_temperature_plot(self.temperature_history, (10, 40), (200, 80))
                self.draw_speed_histogram(speeds, (10, 140), (200, 80), self.bin_gap)
                self.draw_count_plot(self.particle_count, (10, 240), (200, 80))

        if self.show_help:
            self.draw_help_popup()
        if not self.is_menu:
            pygame.display.flip()
         
    def draw_ui(self):

        header_y = 10
        status_y = 340
        # Particle count
        text = self.font.render(f"Particle count: {len(self.particles)}", True, (225, 225, 225))
        self.screen.blit(text, (10, header_y))
        
        # Particle size
        text = self.font.render(f"Particle size: {self.particle_radius}", True, (200,200,200))
        self.screen.blit(text, (250, header_y))

        # Time
        text = self.font.render(f"Time : {self.time:.2f}", True, (200,200,200))
        self.screen.blit(text, (self.width - 200, header_y))

        # Time scale
        text = self.small_font.render(f"Time Scale: {self.time_scale} x", True, (225, 225, 225))
        self.screen.blit(text, (10, status_y))
        
        # Damping status (color changes based on state)
        damping_color = (0, 255, 0) if self.damping else (255, 0, 0)
        text = self.small_font.render(f"Damping: {'ON' if self.damping else 'OFF'}", True, damping_color)
        self.screen.blit(text, (10, status_y + 20))
        
        # Gravity status (color changes based on state)
        gravity_color = (0, 255, 0) if self.gravity else (255, 0, 0)
        text = self.small_font.render(f"Gravity: {'ON' if self.gravity else 'OFF'}", True, gravity_color)
        self.screen.blit(text, (10, status_y + 40))

        # Evaporation status (color changes based on state)
        evap_color = (0, 255, 0) if self.evaporation else (255, 0, 0)
        text = self.small_font.render(f"Evaporation: {'ON' if self.evaporation else 'OFF'}", True, evap_color)
        self.screen.blit(text, (10, status_y + 60))

        # Particle Damping status (color changes based on state)
        pardamp_color = (0, 255, 0) if self.collision_damping else (255, 0, 0)
        text = self.small_font.render(f"Collision Damping: {'ON' if self.collision_damping else 'OFF'}", True, pardamp_color)
        self.screen.blit(text, (10, status_y + 80))
    
    def draw_energy_plot(self, data, pos, size):
        x0, y0 = pos
        w, h = size
        
        # Draw plot border
        border_color = (200, 200, 200)
        pygame.draw.rect(self.screen, border_color, (x0, y0, w, h), 1)
        
        if not data:
            return
        
        max_energy = max(data) or 1  # avoid division by zero
        
        # Draw zero line (bottom of plot)
        pygame.draw.line(self.screen, (100, 100, 100), (x0, y0 + h), (x0 + w, y0 + h), 1)
        
        # Labels
        max_label = self.small_font.render(f"{max_energy:.1f}", True, (200, 200, 200))
        self.screen.blit(max_label, (x0 + 2, y0 + 2))
        
        curr_label = self.small_font.render(f"{data[-1]:.2f}", True, (200, 200, 200))
        self.screen.blit(curr_label, (x0 + 2, y0 + 12))
        
        # Plot the energy line
        for i in range(1, len(data)):
            x1 = x0 + (i - 1) * w / self.max_history
            y1 = y0 + h - (data[i - 1] / max_energy * h)
            x2 = x0 + i * w / self.max_history
            y2 = y0 + h - (data[i] / max_energy * h)
            pygame.draw.line(self.screen, (0, 255, 0), (x1, y1), (x2, y2), 2)
    
    def draw_temperature_plot(self, data, pos, size):
        x0, y0 = pos
        w, h = size
        
        # Draw plot border
        border_color = (200, 200, 200)
        pygame.draw.rect(self.screen, border_color, (x0, y0, w, h), 1)
        
        if not data:
            return
        
        if not self.particles:
            task_label = self.small_font.render("TEMPERATURE", True, (200, 200, 200))
            task_label_w, task_label_h = task_label.get_width(), task_label.get_height()
            self.screen.blit(task_label, (x0 + w//2 - task_label_w//2, y0 + h//2 - task_label_h//2))
            max_label = self.small_font.render(f"MAX", True, (200, 200, 200))
            self.screen.blit(max_label, (x0 + 2, y0 + 2))
            curr_label = self.small_font.render(f"CURRENT", True, (200, 200, 200))
            curr_label_width = curr_label.get_width()
            self.screen.blit(curr_label, (x0 + w - curr_label_width - 2, y0 + 2))

        max_temp = max(data) or 1  # avoid division by zero
        
        # Draw zero line (bottom of plot)
        pygame.draw.line(self.screen, (100, 100, 100), (x0, y0 + h), (x0 + w, y0 + h), 1)
        
        # Plot the temperature line
        for i in range(1, len(data)):
            x1 = x0 + (i - 1) * w / self.max_history
            y1 = y0 + h - (data[i - 1] / max_temp * h)
            x2 = x0 + i * w / self.max_history
            y2 = y0 + h - (data[i] / max_temp * h)
            pygame.draw.line(self.screen, (255, 0, 0), (x1, y1), (x2, y2), 2)

        # Labels
        if self.particles:
            max_label = self.small_font.render(f"{max_temp:.1f}", True, (200, 200, 200))
            self.screen.blit(max_label, (x0 + 2, y0 + 2))
            
            curr_label = self.small_font.render(f"{data[-1]:.2f}", True, (200, 200, 200))
            curr_label_width = curr_label.get_width()
            self.screen.blit(curr_label, (x0 + w - curr_label_width - 2, y0 + 2))

    def draw_count_plot(self, counts, pos, size):
        x0,y0 = pos 
        w,h = size 

        border_color = (200,200,200)
        pygame.draw.rect(self.screen, border_color, (x0, y0, w, h), 1)

        if not counts:
            return 

        if not self.particles:
            task_label = self.small_font.render("PARTICLE COUNT", True, (200, 200, 200))
            task_label_w, task_label_h = task_label.get_width(), task_label.get_height()
            self.screen.blit(task_label, (x0 + w//2 - task_label_w//2, y0 + h//2 - task_label_h//2))
            max_label = self.small_font.render(f"MAX", True, (200, 200, 200))
            self.screen.blit(max_label, (x0 + 2, y0 + 2))
            curr_label = self.small_font.render(f"CURRENT", True, (200, 200, 200))
            curr_label_width = curr_label.get_width()
            self.screen.blit(curr_label, (x0 + w - curr_label_width - 2, y0 + 2))

        max_temp = max(counts) or 1  # avoid division by zero
        
        # Draw zero line (bottom of plot)
        pygame.draw.line(self.screen, (100, 100, 100), (x0, y0 + h), (x0 + w, y0 + h), 1)

        # Plot the energy line
        for i in range(1, len(counts)):
            x1 = x0 + (i - 1) * w / self.max_history
            y1 = y0 + h - (counts[i - 1] / max_temp * h)
            x2 = x0 + i * w / self.max_history
            y2 = y0 + h - (counts[i] / max_temp * h)
            pygame.draw.line(self.screen, (0, 0, 255), (x1, y1), (x2, y2), 2)

        # Labels
        if self.particles:
            max_label = self.small_font.render(f"{max_temp}", True, (200, 200, 200))
            self.screen.blit(max_label, (x0 + 2, y0 + 2))
            
            curr_label = self.small_font.render(f"{counts[-1]}", True, (200, 200, 200))
            curr_label_width = curr_label.get_width()
            self.screen.blit(curr_label, (x0 + w - curr_label_width - 2, y0 + 2))
            
    def draw_speed_histogram(self, speeds, pos, size, bin_gap):
        x0, y0 = pos
        w, h = size
        def select_bin_gap(value):
            if value < 2.5:
                return 0.1
            elif value < 10:
                return 0.5
            elif value < 20:
                return 1
            elif value < 50:
                return 2.5
            elif value < 100:
                return 5
            elif value < 250:
                return 10
            else:
                return 50
            
        # Draw plot border
        border_color = (200, 200, 200)
        pygame.draw.rect(self.screen, border_color, (x0, y0, w, h), 1)
        
        if not speeds:
            # Draw labels even when no particles
            maxcount_label = self.small_font.render(f"MAX COUNT", True, (200, 200, 200))
            min_label = self.small_font.render(f"MIN", True, (200, 200, 200))
            max_label = self.small_font.render(f"MAX", True, (200, 200, 200))
            range_label = self.small_font.render(f"RANGE", True, (200, 200, 200))
            max_label_w = max_label.get_width()
            range_label_w = range_label.get_width()

            self.screen.blit(min_label, (x0 + 2, y0 + h - 12))  # Bottom left (min)
            self.screen.blit(max_label, (x0 + w - max_label_w - 2, y0 + 2))  # Top right (current max)
            self.screen.blit(range_label, (x0 + w - range_label_w - 2, y0 + h - 12)) # Bottom right (overall max)
            self.screen.blit(maxcount_label, (x0 + 2, y0 + 2)) # Top left (overall max)

            task_label = self.small_font.render("SPEED DISTRIBUTION", True, (200, 200, 200))
            task_label_w, task_label_h = task_label.get_width(), task_label.get_height()
            self.screen.blit(task_label, (x0 + w//2 - task_label_w//2, y0 + h//2 - task_label_h//2))
            return
        

        current_min = min(speeds)
        current_max = max(speeds)
        
        # Update overall max speed if needed
        if current_max < 1: 
            self.most_max_speed = 1.0
            self.bin_gap = 0.1

        if current_max > self.most_max_speed:
            self.most_max_speed = current_max
            if not self.bin_gap_overide:
                self.bin_gap = select_bin_gap(self.most_max_speed)

        if (current_max > 1) and (current_max < self.most_max_speed/2):
            self.most_max_speed = current_max
            if not self.bin_gap_overide:
                self.bin_gap = select_bin_gap(self.most_max_speed)
    
        bins = int(self.most_max_speed / bin_gap) + 1
        hist = [0] * bins
        
        for s in speeds:
            index = min(int(s / self.most_max_speed * bins), bins - 1)
            hist[index] += 1
        
        max_count = max(hist) or 1
        bin_width = max(1,w / bins)
        
        # Draw histogram bars
        for i in range(bins):
            bar_height = (hist[i] / max_count) * h
            bar_x = x0 + i * bin_width
            bar_y = y0 + h - bar_height
            pygame.draw.rect(
                self.screen,
                (0, 255, 0),
                pygame.Rect(bar_x, bar_y, bin_width - 1, bar_height)
            )
        
        # Draw min and max labels
        maxcount_label = self.small_font.render(f"{max_count}", True, (200, 200, 200))
        min_label = self.small_font.render(f"{current_min:.1f}", True, (200, 200, 200))
        max_label = self.small_font.render(f"{current_max:.1f}", True, (200, 200, 200))
        range_label = self.small_font.render(f"{self.most_max_speed:.1f}", True, (200, 200, 200))
        max_label_w = max_label.get_width()
        range_label_w = range_label.get_width()

        self.screen.blit(min_label, (x0 + 2, y0 + h - 12))  # Bottom left (min)
        self.screen.blit(max_label, (x0 + w - max_label_w - 2, y0 + 2))  # Top right (current max)
        self.screen.blit(range_label, (x0 + w - range_label_w - 2, y0 + h - 12)) # Bottom right (overall max)
        self.screen.blit(maxcount_label, (x0 + 2, y0 + 2)) # Top left (overall max)
    
    def calculate_cell_density(self):
        self.cell_density = defaultdict(int)
        for p in self.particles:
            cell = self.get_cell(p.pos)
            self.cell_density[cell] += 1

    def draw_cell_density(self):
        if not self.cell_density:
            return

        max_density = max(self.cell_density.values()) if self.cell_density else 1
        
        for cell, count in self.cell_density.items():
            # Normalize density to [0,1] range
            normalized = count / max_density
            # Get RGBA color (we'll ignore alpha)
            rgba = self.inferno_cmap(normalized)
            # Convert to pygame color (RGB tuple, 0-255 range)
            color = tuple(int(255 * x) for x in rgba[:3])
            
            cell_rect = pygame.Rect(
                cell[0] * self.cell_size,
                cell[1] * self.cell_size,
                self.cell_size,
                self.cell_size
            )
            pygame.draw.rect(self.screen, color, cell_rect)
    
    def draw_help_popup(self):
        if not self.show_help:
            return

        # Calculate popup dimensions
        line_height = 15
        margin = 15
        max_width = max(self.help_font.size(line)[0] for line in self.help_text)
        popup_width = max_width + 2 * margin
        popup_height = len(self.help_text) * line_height + 2 * margin
        
        # Position in center of screen
        popup_x = (self.width - popup_width) // 2
        popup_y = (self.height - popup_height) // 2
        
        # Draw popup background
        pygame.draw.rect(self.screen, (30, 0, 0), 
                        (popup_x, popup_y, popup_width, popup_height))
        pygame.draw.rect(self.screen, (120, 10, 10), 
                        (popup_x, popup_y, popup_width, popup_height), 2)
        
        # Draw text lines
        for i, line in enumerate(self.help_text):
            text_surface = self.help_font.render(line, True, (250, 250, 250))
            self.screen.blit(text_surface, 
                           (popup_x + margin, popup_y + margin + i * line_height))
    # @staticmethod
    def get_cell(self,pos):
        return int(pos.x // self.cell_size), int(pos.y // self.cell_size)

class Particle:
    def __init__(self, x, y, radius, color="random"):
        self.mass = 1
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.dragging = False
        self.trajectory = []
        
        if color == "random":
            r, g, b = self.get_random_color()
        elif color == "red":
            r, g, b = 255, 0, 0
        else:
            r, g, b = 255, 255, 255  # default white
        
        self.original_color = (r, g, b)
        self.color = self.original_color
    
    def get_random_color(self, minimum_color = 35):
        while True:
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            # If not all colors are below min, return this color
            if not (r < minimum_color and g < minimum_color and b < minimum_color):
                return (r, g, b)

    def apply_force(self, force):
        self.acc += force / self.mass
    
    def update(self):
        self.vel += self.acc * sim.time_scale
        self.pos += self.vel * sim.time_scale
        self.acc *= 0  # reset acceleration
        
        # Track trajectory
        self.trajectory.append(self.pos.copy())
        if len(self.trajectory) > 5000:
            self.trajectory.pop(0)
    
    def check_bounds(self, width, height, damping, damping_factor):
        decay_parameter_lr = damping_factor if damping else 1
        decay_parameter_ud = damping_factor if damping else 1
        
        # Left and right walls
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x *= -1 * decay_parameter_lr
        elif self.pos.x + self.radius >= width:
            self.pos.x = width - self.radius
            self.vel.x *= -1 * decay_parameter_lr
        
        # Top and bottom walls
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y *= -1 * decay_parameter_ud
        elif self.pos.y + self.radius >= height:
            self.pos.y = height - self.radius
            self.vel.y *= -1 * decay_parameter_ud
    
    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

# Create and run simulation
if __name__ == "__main__":
    sim = Simulation(1000, 600)
    sim.run()