import pygame 
import sys 
import math

pygame.init()
screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Partikol")
clock = pygame.time.Clock()
background_color = (10, 10, 10)
G_const = 5
time_scale = 1

screen_center = pygame.math.Vector2(screen.get_width() / 2, screen.get_height() / 2)
camera_mode = "neutral"
class Star:
    def __init__(self, x, y, fixed = True,  radius = 10, color=(255, 255, 0)):
        self.mass = 50
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.collision_radius = radius
        self.color = color
        self.original_color = self.color
        self.dragging = False
        self.collision = False
        self.fixed = fixed
        self.trajectory = []  # FIXED: initialize trajectory list
        self.true_trajectory = []

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self):
        if not self.fixed:
            self.vel += self.acc 
            self.pos += self.vel
        self.acc *= 0  # reset acceleration after applying
        self.true_trajectory.append(self.pos.copy())
        reference_center = get_reference_frame(camera_mode)
        self.trajectory.append((self.pos - reference_center).copy())
        if len(self.trajectory) > 5000:
            self.trajectory.pop(0)

    def trajectory_plot(self, screen, camera_center, screen_center, zoom, color=(200, 200,0), skip=1):
        if camera_mode == "neutral":
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos - camera_center) * zoom + screen_center
                    for pos in self.true_trajectory[::skip]
                ]
                pygame.draw.lines(screen, color, False, transformed_trajectory, 2)
        else:
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos) * zoom + screen_center
                    for pos in self.trajectory[::skip]
                ]
                pygame.draw.lines(screen, color, False, transformed_trajectory, 2)
    def draw(self, screen):
        draw_pos = (self.pos - camera_center) * zoom + screen_center
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)

class Planet:
    def __init__(self, x, y, radius = 2, color=(0, 150, 255)):
        self.mass = 1
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.collision_radius = radius
        self.color = color
        self.original_color = self.color
        self.dragging = False
        self.collision = False
        self.true_trajectory = []
        self.trajectory = []  # FIXED: initialize trajectory list

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self):
        self.vel += self.acc * time_scale 
        self.pos += self.vel * time_scale
        self.acc *= 0
        self.true_trajectory.append(self.pos.copy())
        reference_center = get_reference_frame(camera_mode)
        self.trajectory.append((self.pos - reference_center).copy())
        if len(self.trajectory) > 5000:
            self.trajectory.pop(0)

    def trajectory_plot(self, screen, camera_center, screen_center, zoom, color=(0, 0, 200), skip=1):
        if camera_mode == "neutral":
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos - camera_center) * zoom + screen_center
                    for pos in self.true_trajectory[::skip]
                ]
                pygame.draw.lines(screen, color, False, transformed_trajectory, 2)
        else:
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos) * zoom + screen_center
                    for pos in self.trajectory[::skip]
                ]
                pygame.draw.lines(screen, color, False, transformed_trajectory, 2)

    def draw(self, screen):
        draw_pos = (self.pos - camera_center) * zoom + screen_center
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)
  

class Asteroid:
    pass 

def get_reference_frame(camera_mode):
    if camera_mode == "barycenter":
        total_mass = sum(obj.mass for obj in star_list + planet_list)
        if total_mass > 0:
            return sum(
                (obj.pos * obj.mass for obj in star_list + planet_list),
                pygame.math.Vector2(0, 0)
            ) / total_mass 
    elif camera_mode == "star" and star_list:
        return star_list[0].pos
    elif camera_mode == "neutral":
        return camera_center
    return pygame.math.Vector2(0, 0)

def gravitational_force(body1, body2):
    direction = body2.pos - body1.pos
    distance_sq = direction.length_squared()
    if distance_sq == 0:
        return pygame.math.Vector2(0, 0)
    force_mag = G_const * body1.mass * body2.mass / distance_sq
    force = direction.normalize() * force_mag
    return force

def draw_grid(show_grid):
    if show_grid:
        grid_spacing = 100  # world units between grid lines
        grid_color = (50, 50, 50)  # dim gray

        # Compute the corners of the current screen in world coordinates
        screen_rect = screen.get_rect()
        top_left = (pygame.math.Vector2(0, 0) - screen_center) / zoom + camera_center
        bottom_right = (pygame.math.Vector2(screen_rect.width, screen_rect.height) - screen_center) / zoom + camera_center

        # Round to nearest grid line
        start_x = int(top_left.x // grid_spacing) * grid_spacing
        end_x = int(bottom_right.x // grid_spacing + 1) * grid_spacing
        start_y = int(top_left.y // grid_spacing) * grid_spacing
        end_y = int(bottom_right.y // grid_spacing + 1) * grid_spacing

        # Draw vertical lines
        for x in range(start_x, end_x, grid_spacing):
            start = (pygame.math.Vector2(x, start_y) - camera_center) * zoom + screen_center
            end = (pygame.math.Vector2(x, end_y) - camera_center) * zoom + screen_center
            pygame.draw.line(screen, grid_color, start, end, 1)

        # Draw horizontal lines
        for y in range(start_y, end_y, grid_spacing):
            start = (pygame.math.Vector2(start_x, y) - camera_center) * zoom + screen_center
            end = (pygame.math.Vector2(end_x, y) - camera_center) * zoom + screen_center
            pygame.draw.line(screen, grid_color, start, end, 1)

## Initializations 
star_list = []
planet_list = []
asteroid_list = []

# 
#PERIFOCAL // ROTATING POINT OF VIEW PER PLANET
    ## SUN CENTERED // PLANET CENTERED
#BUG FIXES 
    ## C - key, what's wrong, F key, still moves, B,N,M key, 
    ## center it to 0,0 next time
    ## asteroids, for gravitational testing and L3 L4 spotting
    ## collisions - absorbing or nonabsorbing 
    ## getting rid of the extrasolars,
    ## RK4 the fucker
show_grid = True
zoom = 1.0  # 1.0 = normal size, 2.0 = zoomed in, 0.5 = zoomed out
trac_selected_index = -1
dragging = False
trajectory_plot = True

star_fixed = False
running = True 
camera_mode = "neutral"
camera_center = screen_center
while running:
    screen.fill(background_color)
    mouse_pos = pygame.mouse.get_pos()
    screen_center = pygame.math.Vector2(screen.get_width() / 2, screen.get_height() / 2)
    if camera_mode == "barycenter":
        total_mass = sum(obj.mass for obj in star_list + planet_list)
        if total_mass > 0:
            camera_center = sum(
                (obj.pos * obj.mass for obj in star_list + planet_list),
                pygame.math.Vector2(0, 0)
            ) / total_mass
    elif camera_mode == "star":
        if star_list:
            camera_center = star_list[0].pos

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                planet_list = []
                star_list = []
                asteroid_list = []
            if event.type == pygame.KEYDOWN and event.key == pygame.K_g:
                show_grid = not show_grid
            if event.key == pygame.K_k:
                for s in star_list:
                    s.pos = pygame.math.Vector2(0, 0)
                    s.vel = pygame.math.Vector2(0, 0)
            if event.key == pygame.K_p:
                planet_list = []
                
                for p in star_list + planet_list:
                    p.trajectory = []
                    p.true_trajectory = []
            if event.key == pygame.K_s:
                mx,my = (pygame.math.Vector2(mouse_pos) - screen_center) / zoom + camera_center
                new_star = Star(mx,my, star_fixed)
                ## center_star = Star(screen.get_width()/2, screen.get_height()/2)
                star_list.append(new_star)
            if event.key == pygame.K_x:
                # Compute center of mass of stars
                total_mass = sum(star.mass for star in star_list)
                if total_mass > 0:
                    com = sum((star.pos * star.mass for star in star_list), pygame.math.Vector2(0, 0)) / total_mass
                    offset = screen_center - com

                    # Shift all objects by offset
                    for star in star_list:
                        star.pos += offset
                        star.trajectory = [p + offset for p in star.trajectory]

                    for planet in planet_list:
                        planet.pos += offset
                        planet.trajectory = [p + offset for p in planet.trajectory]
            if event.key == pygame.K_t:
                trajectory_plot = not(trajectory_plot)
            if event.key == pygame.K_EQUALS:  # "+" key
                zoom *= 1.1
            if event.key == pygame.K_MINUS:  # "-" key
                zoom /= 1.1
            shift = screen.get_width() / 32 / zoom  # make shift size zoom-independent
            if event.key == pygame.K_LEFT:
                camera_center.x -= shift
            elif event.key == pygame.K_RIGHT:
                camera_center.x += shift
            elif event.key == pygame.K_UP:
                camera_center.y -= shift
            elif event.key == pygame.K_DOWN:
                camera_center.y += shift
            if event.key == pygame.K_2:
                time_scale += 1
            if event.key == pygame.K_1:
                if time_scale > 1:
                    time_scale -= 1
            if event.key == pygame.K_r:
                for p in planet_list + star_list:
                    p.trajectory = []
                    p.true_trajectory = []
            if event.key == pygame.K_c:
                if not star_list:
                    continue  # no central mass

                mouse_vec = (pygame.math.Vector2(mouse_pos) - camera_center) / zoom + screen_center
                # Find closest star to mouse
                closest_star = min(star_list, key=lambda s: (s.pos - mouse_vec).length_squared())
                r_vec = mouse_vec - closest_star.pos
                r = r_vec.length()

                if r == 0:
                    continue  # avoid division by zero

                # Direction: perpendicular to r_vec
                radial_dir = r_vec.normalize()
                perpendicular = pygame.math.Vector2(-radial_dir.y, radial_dir.x)  # default CCW

                # Determine clockwise or counterclockwise based on mouse position
                center = closest_star.pos
                to_mouse = mouse_vec - center
                cross_z = center.cross(mouse_vec)  # or just radial_dir.cross(to_mouse)
                if cross_z < 0:
                    perpendicular *= -1  # flip to CW

                # Circular velocity magnitude
                v_mag = math.sqrt(G_const * closest_star.mass / r)

                # Create and add planet
                new_planet = Planet(mouse_vec.x, mouse_vec.y)
                new_planet.vel = perpendicular * v_mag
                planet_list.append(new_planet)
            if event.key == pygame.K_b:
                camera_mode = "barycenter"
                for p in star_list + planet_list:
                    p.trajectory = []
                    p.true_trajectory = []
            if event.key == pygame.K_m:
                camera_mode = "star"
                for p in star_list + planet_list:
                    p.trajectory = []
                    p.true_trajectory = []
            if event.key == pygame.K_n:
                camera_mode = "neutral"
                for p in star_list + planet_list:
                    p.trajectory = []
                    p.true_trajectory = []
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            f_pressed = True
            ref_center = get_reference_frame(camera_mode)
            mouse_vec = pygame.math.Vector2(mouse_pos)
            world_pos = (mouse_vec - screen_center) / zoom + ref_center
            p = Planet(world_pos.x, world_pos.y)
            p.dragging = True
            current_particle = p
            dragging = True
            dragging_with_key = True
            planet_list.append(p)
        if event.type == pygame.KEYUP and event.key == pygame.K_f and current_particle and dragging_with_key:
            mx, my = (pygame.math.Vector2(mouse_pos) - screen_center) / zoom + camera_center
            drag_vector = current_particle.pos - pygame.Vector2(mx, my)
            current_particle.vel = drag_vector * 0.05
            current_particle.dragging = False
            current_particle = None
            dragging = False
            dragging_with_key = False
            f_pressed = False
    draw_grid(show_grid)
    # Compute gravitational forces between all planets and stars
    for planet in planet_list:
        if planet.dragging:
            planet.draw(screen)
            continue
        for star in star_list:
            force = gravitational_force(planet, star)
            planet.apply_force(force)
            star.apply_force(-force)  # only moves if not fixed inside method

        for planet2 in planet_list:
            if planet2 is planet:
                continue  # skip self-interaction
            if planet2.dragging:
                continue
            force = gravitational_force(planet, planet2)
            planet.apply_force(force)
            planet2.apply_force(-force)
        planet.update()
        planet.trajectory_plot(screen, camera_center, screen_center, zoom)
        planet.draw(screen)
    # Update and draw all stars
    for star in star_list:
        star.update()
        if not (star_fixed):
            for star2 in star_list:
                if star2 is star:
                    continue  # skip self-interaction
                if star2.dragging:
                    continue
                force = gravitational_force(star, star2)
                star.apply_force(force)
                star2.apply_force(-force)
            star.trajectory_plot(screen, camera_center, screen_center, zoom)
        star.draw(screen)

    if dragging and current_particle:
        pygame.draw.line(
            screen, 
            (255, 0, 0), 
            (current_particle.pos - camera_center) * zoom + screen_center, 
            mouse_pos, 2
        )
        pygame.draw.circle(screen, (0, 200, 200), mouse_pos, 2)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
