import pygame 
import sys 
import math

class Particle():
    def __init__(self, x ,y , mass, radius, color, fixed = False):
        self.mass = mass 
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(0,0)
        self.acc = pygame.math.Vector2(0,0)
        self.radius = radius 
        self.collision_radius = radius
        self.color = color 
        self.dragging = False
        self.collision = False
        self.fixed = fixed
        self.true_trajectory = []
        self.camera_trajectory = []
    
    def apply_force(self, force):
        self.acc += force / self.mass

    def euler_update(self):
        self.vel += self.acc 
        self.pos += self.vel 

    # def rk4_update(self, dt):
    #     if self.fixed:
    #         return
    #     # Store initial conditions
    #     r0 = self.pos
    #     v0 = self.vel
    #     a0 = self.acc  # acceleration = force / mass

    #     # k1
    #     k1_r = v0
    #     k1_v = a0

    #     # k2
    #     k2_r = v0 + 0.5 * dt * k1_v
    #     k2_v = self.compute_acc(r0 + 0.5 * dt * k1_r, v0 + 0.5 * dt * k1_v)

    #     # k3
    #     k3_r = v0 + 0.5 * dt * k2_v
    #     k3_v = self.compute_acc(r0 + 0.5 * dt * k2_r, v0 + 0.5 * dt * k2_v)

    #     # k4
    #     k4_r = v0 + dt * k3_v
    #     k4_v = self.compute_acc(r0 + dt * k3_r, v0 + dt * k3_v)

    #     # Final RK4 integration
    #     self.pos += (dt / 6.0) * (k1_r + 2 * k2_r + 2 * k3_r + k4_r)
    #     self.vel += (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

    def update(self): #, dt, camera_mode):
        if not self.fixed:
            self.euler_update()
        self.acc *= 0
        self.true_trajectory.append(self.pos.copy())
        # reference_center = functions.get_reference_frame(camera_mode)
        #self.trajectory.append((self.pos - reference_center).copy())
        # if len(self.trajectory) > 5000:
        #     self.trajectory.pop(0)

    def trajectory_plot(self, screen,skip=1):
        pass 
    def draw(self, screen):
        global zoom
        draw_pos = world_to_screen(self.pos)
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)

class Star(Particle):
    def __init__(self, x, y, mass = 20, radius = 10, color = (255,255,0), fixed = False):
        super().__init__(x, y, mass, radius, color, fixed)

    def apply_force(self, force):
        super().apply_force(force)

    def euler_update(self):
        super().euler_update()

    def update(self):
        super().update()

    def trajectory_plot(self, screen, skip=1):
        super().trajectory_plot(screen, skip)

    def draw(self, screen):
        super().draw(screen)

class Planet(Particle):
    def __init__(self, x, y, mass = 1, radius = 2, color = (0,0,255)):
        super().__init__(x, y, mass, radius, color)

    def apply_force(self, force):
        super().apply_force(force)

    def update(self):
        super().update()

    def trajectory_plot(self, screen, skip=1):
        super().trajectory_plot(screen, skip)

    def draw(self, screen):
        super().draw(screen)

class Asteroid(Particle):
    def __init__(self, x, y, mass = 0, radius = 1, color = (200,200,200)):
        super().__init__(x, y, mass, radius, color)

    def apply_force(self, force):
        super().apply_force(force)

    def update(self, camera_mode):
        super().update(camera_mode)

    def trajectory_plot(self, screen, skip=1):
        super().trajectory_plot(screen, skip)

    def draw(self, screen):
        super().draw(screen)

## Pygame initialization
pygame.init()
pygame.display.set_caption("Partikol")
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont("Consolas", 12)
clock = pygame.time.Clock()
vec2 = pygame.math.Vector2



## Debug_tools
def draw_mouse_position(screen, font, color=(255, 255, 255), pos=(10, 10)):
    # Screen position of mouse
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (100, 100, 100), (mouse_x, mouse_y), 5)

    # Convert to world position
    mouse_vec = vec2(mouse_x, mouse_y)
    world_pos = screen_to_world(mouse_vec)
    # Render each line separately
    line1 = font.render(f"Mouse (screen): ({mouse_x}, {mouse_y})", True, color)
    line2 = font.render(f"Mouse (world) : ({world_pos.x:.2f}, {world_pos.y:.2f})", True, color)

    # Blit each line
    screen.blit(line1, pos)
    screen.blit(line2, (pos[0], pos[1] + font.get_height()))
def draw_size_circle(screen,screen_center,zoom):
    pygame.draw.circle(screen, (255,0,0), screen_center, 10*zoom)
def draw_center_screen_axis(screen, screen_center):
    screen_width, screen_height = screen.get_rect().size
    pygame.draw.line(screen, (200,0,0), (screen_center.x, 0), (screen_center.x, screen_height), 1)
    pygame.draw.line(screen, (0,200,0), (0, screen_center.y), (screen_width, screen_center.y), 1)

## constants 
background_color = (10,10,10)
zoom, zoom_step = 1.00, 0.1
camera_center = vec2(0, 0)
screen_center = vec2(screen.get_width() / 2, screen.get_height() / 2)
G_const = 1

## Lists
planets = []
stars = []

## Switches 
running = True
show_grid = True
draw_axis = True
fixed = False

def screen_to_world(screen_pos):
    global camera_center, screen_center, zoom
    offset = (screen_pos - screen_center)
    flipped_offset = vec2(offset.x, -offset.y)  # flip Y
    return (flipped_offset + camera_center) / zoom

def world_to_screen(world_pos):
    global camera_center, screen_center, zoom
    unflipped = world_pos * zoom - camera_center 
    flipped = vec2(unflipped.x,-unflipped.y)
    return flipped + screen_center

def Gravitational_Force (body1, body2):
    direction = body2.pos - body1.pos
    distance_sq = direction.length_squared()
    if distance_sq == 0:
        return pygame.math.Vector2(0, 0)
    force_mag = G_const * body1.mass * body2.mass / distance_sq
    force = direction.normalize() * force_mag
    return force

def draw_grid(draw_axis):
    grid_spacing = 100  # scaled grid spacing
    grid_color = (50, 50, 50)

    # Compute visible area in world coordinates
    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.size

    # Convert screen corners to world coordinates
    top_left_world = screen_to_world(vec2(0,0))
    bottom_right_world = screen_to_world(vec2(screen_width,screen_height))
    
    # Snap to grid lines
    start_x = int(top_left_world.x // grid_spacing - 1) * grid_spacing
    end_x = int(bottom_right_world.x // grid_spacing + 1) * grid_spacing
    start_y = int(top_left_world.y // grid_spacing  + 1) * grid_spacing
    end_y = int(bottom_right_world.y // grid_spacing - 1) * grid_spacing

    for x in range(start_x, end_x, grid_spacing):
        sx = world_to_screen(vec2(x, 0))
        pygame.draw.line(screen, grid_color, (sx.x, 0), (sx.x, screen_height), 1)

    for y in range(end_y, start_y, grid_spacing):
        sy = world_to_screen(vec2(0, y))
        pygame.draw.line(screen, grid_color, (0, sy.y), (screen_width, sy.y), 1)
    
    if draw_axis:
        # X-axis (y = 0)
        x_axis_start = world_to_screen(vec2(start_x,0))
        x_axis_end   = world_to_screen(vec2(end_x,0))
        pygame.draw.line(screen, (200, 200, 200), x_axis_start, x_axis_end, 1)

        # Y-axis (x = 0)
        y_axis_start = world_to_screen(vec2(0,start_y))
        y_axis_end   = world_to_screen(vec2(0,end_y))
        pygame.draw.line(screen, (200, 200, 200), y_axis_start, y_axis_end, 1)

def keypress_events():
    global show_grid
    global zoom 
    global running 
    global planets 
    global stars 

    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_DELETE:
                running = False
            if event.key == pygame.K_g:
                show_grid = not show_grid

            elif event.key == pygame.K_EQUALS:  # Zoom in
                zoom *= 1 + zoom_step
            elif event.key == pygame.K_MINUS:   # Zoom out
                zoom *= 1 - zoom_step

            shift = screen.get_width() / 32 / zoom  # make shift size zoom-independent
            if event.key == pygame.K_LEFT:
                camera_center.x -= shift
            elif event.key == pygame.K_RIGHT:
                camera_center.x += shift
            elif event.key == pygame.K_UP:
                camera_center.y += shift
            elif event.key == pygame.K_DOWN:
                camera_center.y -= shift
            elif event.key == pygame.K_a:
                camera_center.x, camera_center.y = (0,0)
                zoom = 1
            
            if event.key == pygame.K_BACKSPACE:
                planets = []
                stars = []
            
            if event.key == pygame.K_s:
                sx, sy = screen_to_world(mouse_pos)
                new_star = Star(sx,sy)
                stars.append(new_star)
            if event.key == pygame.K_x:
                # Compute center of mass of stars
                total_mass = sum(star.mass for star in stars)
                if total_mass > 0:
                    com = sum((star.pos * star.mass for star in stars), pygame.math.Vector2(0, 0)) / total_mass
                    offset = screen_to_world(screen_center) - com
                    for star in stars:
                        star.pos += offset
                        # star.trajectory = [p + offset for p in star.trajectory]
                    for planet in planets:
                        planet.pos += offset
                        # planet.trajectory = [p + offset for p in planet.trajectory]

def particle_updating():
    if show_grid:
        draw_grid(draw_axis= True)
    for p in planets:
        pass 
    for s in stars:
        s.update()
        s.draw(screen)



## ******************************************
##              MAIN GAME LOOP
## ******************************************
while running:
    screen.fill(background_color)
    keypress_events()
    particle_updating()
    ## debug 
    draw_mouse_position(screen, font)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()


