import pygame
import sys
import random 
from collections import defaultdict

pygame.init()
font = pygame.font.SysFont("Consolas", 16)  # (font name=None for default, size=24)

energy_history = []
MAX_HISTORY = 200  # how many frames to keep
CELL_SIZE = 40
most_max_speed = 1.0

def draw_speed_histogram(surface, speeds, pos, size, bin_gap=5):
    global most_max_speed
    x0, y0 = pos
    w, h = size
    border_color = (200, 200, 200)    # Draw plot border
    pygame.draw.rect(surface, border_color, (x0, y0, w, h), 1)
    if not speeds:
        return
 

    # Draw zero line (bottom of plot)
    pygame.draw.line(surface, (200, 200, 200), (x0, y0 + h), (x0 + w, y0 + h), 1)
    max_speed = max(speeds)
    if max_speed == 0:
        max_speed = 1
    if max_speed > most_max_speed:
        most_max_speed = max_speed
    bins = int(most_max_speed / bin_gap) + 1
    hist = [0] * bins
    for s in speeds:
        index = min(int(s / max_speed * bins), bins - 1)
        hist[index] += 1
    max_count = max(hist) or 1
    bin_width = w / bins
    font = pygame.font.SysFont("Consolas", 12)
    max_label = font.render(f"{most_max_speed:.1f}", True, (200, 200, 200))
    surface.blit(max_label, (x0 + 2, y0 + 2))
    for i in range(bins):
        bar_height = (hist[i] / max_count) * h
        bar_x = x0 + i * bin_width
        bar_y = y0 + h - bar_height
        pygame.draw.rect(
            surface,
            (255, 255, 0),
            pygame.Rect(bar_x, bar_y, bin_width - 1, bar_height)
        )

def draw_energy_plot(surface, data, pos, size):
    x0, y0 = pos
    w, h = size
    # Draw plot border
    border_color = (200, 200, 200)
    pygame.draw.rect(surface, border_color, (x0, y0, w, h), 1)
    if not data:
        return

    max_energy = max(data)
    if max_energy == 0:
        max_energy = 1  # avoid div by zero

    

    # Draw zero line (bottom of plot)
    pygame.draw.line(surface, (100, 100, 100), (x0, y0 + h), (x0 + w, y0 + h), 1)

    # Optional: Add text labels (requires a font initialized)
    font = pygame.font.SysFont("Consolas", 12)
    max_label = font.render(f"{max_energy:.1f}", True, (200, 200, 200))
    surface.blit(max_label, (x0 + 2, y0 + 2))

    curr_label = font.render(f"{data[-1]:.2f}", True, (200, 200, 200))
    surface.blit(curr_label, (x0 + 2, y0 + 12))
    # Plot the energy line
    for i in range(1, len(data)):
        x1 = x0 + (i - 1) * w / MAX_HISTORY
        y1 = y0 + h - (data[i - 1] / max_energy * h)
        x2 = x0 + i * w / MAX_HISTORY
        y2 = y0 + h - (data[i] / max_energy * h)
        pygame.draw.line(surface, (0, 255, 0), (x1, y1), (x2, y2), 2)


def get_cell(pos):
    return int(pos.x // CELL_SIZE), int(pos.y // CELL_SIZE)

class Particle:
    def __init__(self, x, y, radius, color = "random"):
        self.mass = 1
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.collision_radius = 2 * radius
        if color == "random":
            r,g,b = random.randint(0,255), random.randint(0,255), random.randint(0,255) 
        elif color == "red":
            r,g,b = 255,0,0
        self.original_color = (r, g, b)  # store original color
        self.color = self.original_color
        self.dragging = False
        self.trajectory = []

    def apply_force(self, force):
        self.acc += force / self.mass

    def update(self):
        self.vel += self.acc * time_scale
        self.pos += self.vel * time_scale 
        self.acc *= 0  # reset acceleration after applying
        # Track full trajectory
        self.trajectory.append(self.pos.copy())
        # Optional: limit size if needed
        if len(self.trajectory) > 5000:
            self.trajectory.pop(0)

    def check_bounds(self, width, height):
        global damping 
        global damping_factor

        if not damping:
            decay_parameter_lr = 1
            decay_parameter_ud = 1
        else:
            decay_parameter_lr = damping_factor
            decay_parameter_ud = damping_factor
        # Left and right wall
        
        if self.pos.x - self.radius <= 0:
            self.pos.x = self.radius
            self.vel.x *= -1 * decay_parameter_lr
        elif self.pos.x + self.radius >= width:
            self.pos.x = width - self.radius
            self.vel.x *= -1 * decay_parameter_lr

        # Top and bottom wall
        if self.pos.y - self.radius <= 0:
            self.pos.y = self.radius
            self.vel.y *= -1 * decay_parameter_ud
        elif self.pos.y + self.radius >= height:
            self.pos.y = height - self.radius
            self.vel.y *= -1 * decay_parameter_lr

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)

gravity_acc = 0.5
gravity = False

damping = False 
damping_factor = 0.9

time_scale = 1 
time_step = 2

selected_index = -1
trajectory_points = []

screen = pygame.display.set_mode((1000, 600))
pygame.display.set_caption("Partikol")
clock = pygame.time.Clock()

running = True
particles = []
dragging = False
current_particle = None
dragging_with_key = False  # track if 'F' was used
f_pressed = False

draw_plots = True 
while running:
    screen.fill((10, 10, 10))  # Dark gray background
    mouse_pos = pygame.mouse.get_pos()
    # print(mouse_pos)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE: ## Clear all particles
                particles = []
                trajectory_points = []
                selected_index = -1
                time_scale = 1

            if event.key == pygame.K_ESCAPE:
                running = False
            if event.key == pygame.K_r:
                width, height = screen.get_size()
                new_particles = []
                for _ in range(100):
                    x = random.randint(0, width)
                    y = random.randint(0, height)
                    p = Particle(x, y, radius=5)  
                    new_particles.append(p)
                particles.extend(new_particles)  # add to existing list
            if event.key == pygame.K_c:
                mx, my = pygame.mouse.get_pos()
                count, attempts = 0,0
                max_attempts = 400
                while count < 100 and attempts < max_attempts:
                    attempts += 1
                    x = random.randint(mx - 100, mx + 100)
                    y = random.randint(my - 100, my + 100)

                    if (mx - x)**2 + (my - y)**2 < 100**2:
                        # Clamp to screen bounds
                        x = max(0, min(x, screen.get_width()))
                        y = max(0, min(y, screen.get_height()))
                        p = Particle(x, y, radius=5)
                        particles.append(p)
                        count += 1
            if event.key == pygame.K_g:
                gravity = not(gravity)
            if event.key == pygame.K_LEFT:
                if particles:
                    selected_index = (selected_index - 1) % len(particles)
                    trajectory_points = []
            elif event.key == pygame.K_RIGHT:
                if particles:
                    selected_index = (selected_index + 1) % len(particles)
                    trajectory_points = []
            elif event.key == pygame.K_DOWN:
                if particles:
                    trajectory_points = []
                    selected_index = -1
            if event.key == pygame.K_d: 
                damping = not damping
            if event.key == pygame.K_COMMA:
                time_scale /= time_step
            if event.key == pygame.K_PERIOD:
                time_scale *= time_step

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            p = Particle(*event.pos, radius=5)
            p.dragging = True
            current_particle = p
            dragging = True
            particles.append(p)

       
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and current_particle:
            drag_vector = current_particle.pos - pygame.Vector2(event.pos)
            current_particle.vel = drag_vector * 0.1  # scale factor
            current_particle.dragging = False
            current_particle = None
            dragging = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_pos = pygame.Vector2(event.pos)
            for p in particles:
                direction = p.pos - mouse_pos
                distance = direction.length()
                if distance < 50 and distance > 0:
                    force_magnitude = 50   # inverse-distance repulsion
                    repulsive_force = direction.normalize() * force_magnitude
                    p.apply_force(repulsive_force)
        
        if event.type == pygame.KEYDOWN and event.key == pygame.K_f:
            f_pressed = True
            mx, my = pygame.mouse.get_pos()
            p = Particle(mx, my, radius=5)
            p.dragging = True
            current_particle = p
            dragging = True
            dragging_with_key = True
            particles.append(p)

        # ⌨ F key release = throw
        if event.type == pygame.KEYUP and event.key == pygame.K_f and current_particle and dragging_with_key:
            mx, my = pygame.mouse.get_pos()
            drag_vector = current_particle.pos - pygame.Vector2(mx, my)
            current_particle.vel = drag_vector * 0.1
            current_particle.dragging = False
            current_particle = None
            dragging = False
            dragging_with_key = False
            f_pressed = False
    # Spatial hashing setup
    spatial_hash = defaultdict(list)
    for p in particles:
        cell = get_cell(p.pos)
        spatial_hash[cell].append(p)

    neighbor_offsets = [(-1, -1), (-1, 0), (-1, 1),
                        (0, -1), (0, 0), (0, 1),
                        (1, -1), (1, 0), (1, 1)]

    for p in particles:
        if not p.dragging:
            if gravity:
                p.apply_force(pygame.Vector2(0, 0.2)) # gravity
            else:
                p.apply_force(pygame.Vector2(0, 0))
        p.update()
        p.color = p.original_color
        if 0 <= selected_index < len(particles):
            selected_particle = particles[selected_index]

            # Change color to white
            selected_particle.color = (255, 255, 255)

            # Print
            skip = 2
            if len(selected_particle.trajectory) > 1:
                pygame.draw.lines(screen, (200, 200, 255), False, selected_particle.trajectory[::skip], 2)

        p.check_bounds(screen.get_width(), screen.get_height())
        p.draw(screen)

    # Collision loop (efficient)
    for p1 in particles:
        cell_x, cell_y = get_cell(p1.pos)
        for dx, dy in neighbor_offsets:
            neighbor_cell = (cell_x + dx, cell_y + dy)
            for p2 in spatial_hash.get(neighbor_cell, []):
                if p1 is p2 or p1.dragging or p2.dragging:
                    continue
                delta = p1.pos - p2.pos
                dist = delta.length()
                if 0 < dist < p1.collision_radius:
                    direction = delta.normalize()
                    overlap = p1.collision_radius - dist
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

                    p1.vel = v1n_after * normal + v1t * tangent
                    p2.vel = v2n_after * normal + v2t * tangent
    kinetic_energy = 0
    speeds = []
    for p in particles:
        v = p.vel.length()
        speeds.append(v)
        kinetic_energy += 0.5 * p.mass * v**2

    energy_history.append(kinetic_energy)

    if len(energy_history) > MAX_HISTORY:
        energy_history.pop(0)
        
    if dragging and current_particle:
        pygame.draw.line(screen, (255, 0, 0), current_particle.pos, mouse_pos, 2)
        pygame.draw.circle(screen, (0, 200, 200), mouse_pos, 2)

    text = font.render(f"Particle count: {len(particles)}", True, (225, 225, 225))  # white color
    screen.blit(text, (10, 10))  # top-left corner
    text = font.render(f"Time Scale : {time_scale}", True, (225, 225, 225))  # white color
    screen.blit(text, (10, 250))  # top-left corner
    text = font.render(f"Damping : {'ON' if damping else 'OFF'}", True, (225, 225, 225))
    screen.blit(text, (10, 280))  # top-left corner
    text = font.render(f"Gravity : {'ON' if gravity else 'OFF'}", True, (225, 225, 225))
    screen.blit(text, (10, 310))  # top-left corner
    if draw_plots:
        draw_energy_plot(screen, energy_history, (10, 40), (200, 80))
        draw_speed_histogram(screen, speeds, (10, 140), (200, 80))
    pygame.display.flip()      # Update the screen
    clock.tick(60)

pygame.quit()
sys.exit()