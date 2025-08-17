import pygame 
import sys 
import math

class Particle():
    def __init__(self, x, y, mass, radius, color, fixed=False):
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
        self.being_dragged = False 
    
    def apply_force(self, force):
        self.acc += force / self.mass

    def euler_update(self, dt):
        if not self.fixed:
            self.vel += self.acc * dt
            self.pos += self.vel * dt

    def rk4_update(self, dt):
        if self.fixed:
            return
        # Store initial conditions
        r0 = self.pos
        v0 = self.vel
        a0 = self.acc  # acceleration = force / mass

        # k1
        k1_r = v0
        k1_v = a0

        # k2
        k2_r = v0 + 0.5 * dt * k1_v
        k2_v = self.compute_acc(r0 + 0.5 * dt * k1_r, v0 + 0.5 * dt * k1_v)

        # k3
        k3_r = v0 + 0.5 * dt * k2_v
        k3_v = self.compute_acc(r0 + 0.5 * dt * k2_r, v0 + 0.5 * dt * k2_v)

        # k4
        k4_r = v0 + dt * k3_v
        k4_v = self.compute_acc(r0 + dt * k3_r, v0 + dt * k3_v)

        # Final RK4 integration
        self.pos += (dt / 6.0) * (k1_r + 2 * k2_r + 2 * k3_r + k4_r)
        self.vel += (dt / 6.0) * (k1_v + 2 * k2_v + 2 * k3_v + k4_v)

    def update(self, dt): 
        if self.being_dragged:
            return 
    
        if not self.fixed:
            self.euler_update(dt)
        self.acc *= 0
        
        # Store absolute position
        self.true_trajectory.append(self.pos.copy())
        if len(self.true_trajectory) > 5000:
            self.true_trajectory.pop(0)
        
        # Store camera-relative position based on current mode
        if camera_mode == "barycenter":
            ref_point = calculate_center_of_mass()
        elif camera_mode == "star":
            ref_point = calculate_star_center()
        else:  # free mode
            ref_point = vec2(0, 0)
        
        self.camera_trajectory.append((self.pos - ref_point).copy())
        if len(self.camera_trajectory) > 5000:
            self.camera_trajectory.pop(0)

    def trajectory_plot(self, screen, skip=1):
        # Choose which trajectory to display based on camera mode
        trajectory = self.camera_trajectory if camera_mode != "free" else self.true_trajectory
        
        if len(trajectory) > 1:
            points = []
            for point in trajectory[::skip]:
                if camera_mode == "free":
                    screen_point = world_to_screen(point)
                else:
                    # For relative modes, we need to add back the reference point
                    if camera_mode == "barycenter":
                        ref_point = calculate_center_of_mass()
                    else:
                        ref_point = calculate_star_center()
                    screen_point = world_to_screen(point + ref_point)
                points.append(screen_point)
            
            if len(points) > 1:
                # Draw with semi-transparent color
                trajectory_color = (self.color[0]*0.9, self.color[1]*0.9, self.color[2]*0.9)  # Add alpha
                pygame.draw.lines(screen, trajectory_color, False, points, 1)
    
    def draw(self, screen):
        global zoom
        draw_pos = world_to_screen(self.pos)
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)

class Star(Particle):
    def __init__(self, x, y, mass=200, radius=10, color=(255,255,0), fixed=False):
        super().__init__(x, y, mass, radius, color, fixed)

class Planet(Particle):
    def __init__(self, x, y, mass=1, radius=2, color=(0,0,255)):
        super().__init__(x, y, mass, radius, color)

## Pygame initialization
pygame.init()
pygame.display.set_caption("Grabiti")
screen = pygame.display.set_mode((1000, 600))
font = pygame.font.SysFont("Consolas", 12)
clock = pygame.time.Clock()
vec2 = pygame.math.Vector2

## constants 
background_color = (10,10,10)
zoom, zoom_step = 1.00, 0.1
camera_center = vec2(0, 0)
screen_center = vec2(screen.get_width() / 2, screen.get_height() / 2)
G_const = 5000  # Increased for better visibility
time_scale = 1
delta_t = 1/60
physics_steps = 10  # Number of physics steps per frame

## Lists
particles = []
stars = []
planets = []

## Switches 
running = True
show_grid = True
draw_axis = True
fixed = False
camera_mode = "free"  # "star" or "barycenter"
draw_trajectories = True
paused = False

planet_dragging = False
new_planet = None
drag_start_pos = None

absorption_enabled = True  # Toggle with 'o' key
absorption_radius_mode = "area"  # 'area' or 'linear'

## Frame dragging
right_dragging = False
left_dragging = False
right_drag_start = vec2(0,0)
left_drag_start = vec2(0,0)
camera_drag_start = vec2(0,0)
dragged_particle = None

## Debug_tools
def draw_mouse_position(screen, font, color=(255, 255, 255), pos=(10, 10)):
    global zoom
    mouse_x, mouse_y = pygame.mouse.get_pos()
    pygame.draw.circle(screen, (100, 100, 100), (mouse_x, mouse_y), 5)

    world_pos = screen_to_world(vec2(mouse_x, mouse_y))
    
    line1 = font.render(f"Mouse (screen) : ({mouse_x}, {mouse_y})", True, color)
    line2 = font.render(f"Mouse (world)  : ({world_pos.x:.2f}, {world_pos.y:.2f})", True, color)
    line3 = font.render(f"Zoom           : {zoom:.3f}", True, color)
    line4 = font.render(f"Time scale     : {time_scale:.2f}x", True, color)
    line5 = font.render(f"Camera mode    : {camera_mode}", True, color)
    line6 = font.render(f"Camera center  : ({camera_center.x:.2f}, {camera_center.y:.2f})", True, color)
    line7 = font.render(f"Particle Count : {len(particles)}", True, color)
    line8 = font.render(f"Star Count     : {len(stars)}", True, color)
    line9 = font.render(f"Planet Count   : {len(planets)}", True, color)
    screen.blit(line1, pos)
    screen.blit(line2, (pos[0], pos[1] + font.get_height()))
    screen.blit(line3, (pos[0], pos[1] + 2*font.get_height()))
    screen.blit(line4, (pos[0], pos[1] + 3*font.get_height()))
    screen.blit(line5, (pos[0], pos[1] + 4*font.get_height()))
    screen.blit(line6, (pos[0], pos[1] + 5*font.get_height()))
    screen.blit(line7, (pos[0], pos[1] + 6*font.get_height()))
    screen.blit(line8, (pos[0], pos[1] + 7*font.get_height()))
    screen.blit(line9, (pos[0], pos[1] + 8*font.get_height()))

def draw_center_screen_axis(screen, screen_center):
    screen_width, screen_height = screen.get_rect().size
    pygame.draw.line(screen, (200,0,0), (screen_center.x, 0), (screen_center.x, screen_height), 1)
    pygame.draw.line(screen, (0,200,0), (0, screen_center.y), (screen_width, screen_center.y), 1)

def screen_to_world(screen_pos):
    global camera_center, screen_center, zoom
    offset = (screen_pos - screen_center) / zoom
    return vec2(camera_center.x + offset.x, 
               camera_center.y - offset.y)  # Note y-axis flip

def world_to_screen(world_pos):
    global camera_center, screen_center, zoom
    offset = vec2(world_pos.x - camera_center.x, 
                 camera_center.y - world_pos.y) * zoom
    return offset + screen_center

def calculate_center_of_mass():
    total_mass = 0
    com = vec2(0, 0)
    for particle in particles:
        total_mass += particle.mass
        com += particle.pos * particle.mass
    if total_mass > 0:
        com /= total_mass
    return com

def calculate_star_center():
    if stars:
        center = vec2(0, 0)
        for star in stars:
            center += star.pos
        center /= len(stars)
        return center
    elif particles:
       # Fallback to heaviest particle
        heaviest = max(particles, key=lambda p: p.mass)
        return heaviest.pos
    return vec2(0, 0)

def update_camera_center():
    global camera_center
    if camera_mode == "barycenter":
        com = calculate_center_of_mass()
        camera_center = com 
    elif camera_mode == "star":
        star_center = calculate_star_center()
        camera_center = star_center 
    elif camera_mode == "free":
        camera_center = camera_center

def Gravitational_Force(body1, body2):
    direction = body2.pos - body1.pos
    distance_sq = direction.length_squared()
    ## NO CENTER CALCULATION
    if distance_sq < (body1.radius + body2.radius)**2:
        return vec2(0, 0)  # Skip force calculation if bodies are touching
    if distance_sq == 0:
        return vec2(0, 0)
    force_mag = G_const * body1.mass * body2.mass / distance_sq
    force = direction.normalize() * force_mag
    return force

def draw_grid(draw_axis):
    grid_spacing = 100  # scaled grid spacing
    grid_color = (50, 50, 50)

    screen_rect = screen.get_rect()
    screen_width, screen_height = screen_rect.size

    top_left_world = screen_to_world(vec2(0,0))
    bottom_right_world = screen_to_world(vec2(screen_width,screen_height))
    
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
        x_axis_start = world_to_screen(vec2(start_x,0))
        x_axis_end   = world_to_screen(vec2(end_x,0))
        pygame.draw.line(screen, (200, 200, 200), x_axis_start, x_axis_end, 1)

        y_axis_start = world_to_screen(vec2(0,start_y))
        y_axis_end   = world_to_screen(vec2(0,end_y))
        pygame.draw.line(screen, (200, 200, 200), y_axis_start, y_axis_end, 1)

def mouse_events(event):
    global show_grid, zoom, running, planets, stars, particles
    global right_dragging, camera_center, right_drag_start, left_drag_start
    global camera_drag_start, planet_dragging, drag_start_pos, new_planet
    
    mouse_pos = pygame.mouse.get_pos()
    world_pos = screen_to_world(vec2(mouse_pos))
    
    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.button == 3:  # Right mouse button
            right_dragging = True
            right_drag_start = vec2(mouse_pos)
            camera_drag_start = camera_center.copy()
        if event.button == 1:  # Left mouse button - planet creation
            # Create new planet at mouse position
            new_planet = Planet(world_pos.x, world_pos.y)
            planets.append(new_planet)
            particles.append(new_planet)
            planet_dragging = True
            drag_start_pos = world_pos
            if new_planet:
                new_planet.being_dragged = True

    elif event.type == pygame.MOUSEBUTTONUP:
        if event.button == 3:  # Right mouse button
            right_dragging = False

        if event.button == 1 and planet_dragging:  #LMB # Release planet
            if new_planet:
                # Set velocity based on drag direction and distance
                drag_end_pos = world_pos
                drag_vector = (drag_start_pos - drag_end_pos) * 0.5  # Velocity scale factor
                new_planet.vel = drag_vector
                new_planet.being_dragged = False
                
            planet_dragging = False
            new_planet = None
            drag_start_pos = None
            

        elif event.button == 4:  # Scroll up - zoom in
            zoom *= 1.1

        elif event.button == 5:  # Scroll down - zoom out
            zoom /= 1.1

    elif event.type == pygame.MOUSEMOTION:
        if right_dragging:
            mouse_delta = (vec2(mouse_pos) - right_drag_start)
            camera_center = camera_drag_start - vec2(mouse_delta.x, -mouse_delta.y) / zoom
        elif left_dragging and dragged_particle:
            # Move the dragged particle
            new_world_pos = screen_to_world(vec2(mouse_pos))
            dragged_particle.pos = new_world_pos
            dragged_particle.vel = vec2(0, 0)  # Reset velocity when dragging
            dragged_particle.being_dragged = True

def calculate_circular_velocity(planet_pos, star_pos, star_mass):

    r_vec = planet_pos - star_pos
    distance = r_vec.length()
    if distance == 0:
        return vec2(0, 0)  # Avoid division by zero
    
    # Calculate orbital velocity magnitude (v = sqrt(G*M/r))
    speed = math.sqrt(G_const * star_mass / distance)
    
    # Get perpendicular direction (counter-clockwise)
    tangent = vec2(-r_vec.y, r_vec.x).normalize()
    
    return tangent * speed

def find_orbital_reference(world_pos):
    if stars:
        if camera_mode == "barycenter":
            ref_pos = calculate_center_of_mass()
            ref_mass = sum(s.mass for s in stars)
        elif camera_mode == "star":
            ref_pos = calculate_star_center()
            ref_mass = sum(s.mass for s in stars) / len(stars)
        else:  # free mode
            closest_star = min(stars, key=lambda s: (s.pos - world_pos).length())
            ref_pos = closest_star.pos
            ref_mass = closest_star.mass
    elif planets:  # Fallback to heaviest planet
        heaviest_planet = max(planets, key=lambda p: p.mass)
        ref_pos = heaviest_planet.pos
        ref_mass = heaviest_planet.mass
    else:  # No celestial bodies exist
        return None, None
        
    return ref_pos, ref_mass

def remove_offscreen_particles():
    # Make copies of lists since we'll be modifying them
    particles_copy = particles.copy()
    planets_copy = planets.copy()
    for particle in particles_copy:
        if is_offscreen(particle):
            # Remove from all relevant lists
            if particle in particles:
                particles.remove(particle)
            if particle in planets and particle in planets_copy:
                planets.remove(particle)
            if isinstance(particle, Star) and particle in stars:
                stars.remove(particle)
    for p in particles:
        p.true_trajectory = []
        p.camera_trajectory = []

def keypress_events(event):
    global show_grid, zoom, running, particles, stars, planets
    global camera_mode, time_scale, draw_trajectories, paused, camera_mode, absorption_enabled
    
    mouse_pos = pygame.mouse.get_pos()
    world_pos = screen_to_world(vec2(mouse_pos))
    shift = screen.get_width() / 32 / zoom  # make shift size zoom-independent

    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_DELETE:
            running = False
        if event.key == pygame.K_SPACE:  # Toggle pause
            paused = not paused
        elif event.key == pygame.K_g:
            show_grid = not show_grid
        elif event.key == pygame.K_EQUALS:  # Zoom in
            zoom *= 1 + zoom_step
        elif event.key == pygame.K_MINUS:  # Zoom out
            zoom *= 1 - zoom_step
        elif event.key == pygame.K_LEFT:
            camera_center.x -= shift
        elif event.key == pygame.K_RIGHT:
            camera_center.x += shift
        elif event.key == pygame.K_UP:
            camera_center.y += shift
        elif event.key == pygame.K_DOWN:
            camera_center.y -= shift
        elif event.key == pygame.K_a:  # Reset view and time scale
            camera_center.x, camera_center.y = (0, 0)
            zoom = 1
            time_scale = 1
            camera_mode="free"
        elif event.key == pygame.K_1:
            draw_trajectories = not draw_trajectories
        elif event.key == pygame.K_0:
            for p in particles:
                p.true_trajectory = []
                p.camera_trajectory = []
        elif event.key == pygame.K_BACKSPACE:  # Clear all objects
            particles = []
            stars = []
            planets = []
            time_scale = 1
            camera_mode="free"
        elif event.key == pygame.K_s:  # Add star at mouse position
            new_star = Star(world_pos.x, world_pos.y)
            stars.append(new_star)
            particles.append(new_star)

        elif event.key == pygame.K_9:  # Purge off-screen particles
            remove_offscreen_particles()
        elif event.key == pygame.K_f:  # Add planet with circular orbit
            world_pos = screen_to_world(vec2(mouse_pos))
            new_planet = Planet(world_pos.x, world_pos.y)
            ref_pos, ref_mass = find_orbital_reference(world_pos)
            if ref_pos is not None:  # Only if something exists to orbit
                new_planet.vel = calculate_circular_velocity(world_pos, ref_pos, ref_mass)
            planets.append(new_planet)
            particles.append(new_planet)
        elif event.key == pygame.K_b:  # Barycenter mode
            camera_mode = "barycenter"
            for p in particles:
                p.true_trajectory = []
                p.camera_trajectory = []
            update_camera_center()
        elif event.key == pygame.K_c:  # Star center mode
            camera_mode = "star"
            for p in particles:
                p.true_trajectory = []
                p.camera_trajectory = []
            update_camera_center()
        elif event.key == pygame.K_n:  # Free center mode
            camera_mode = "free"
            for p in particles:
                p.true_trajectory = []
                p.camera_trajectory = []
            update_camera_center()
        elif event.key == pygame.K_COMMA:  # Slow down time
            time_scale = max(0.001, time_scale * 0.9)
        elif event.key == pygame.K_PERIOD:  # Speed up time
            time_scale = min(1000, time_scale * 1.1)
        elif event.key == pygame.K_SLASH:  # Speed up time
            time_scale = 1
        elif event.key == pygame.K_8:  # Recenter main star
            recenter_star()
        elif event.key == pygame.K_o:  # Toggle planet absorption
            absorption_enabled = not absorption_enabled
            status = "ENABLED" if absorption_enabled else "DISABLED"
            print(f"Planet absorption {status}")

def recenter_star():
    if not stars:
        return
    
    # Find the first/main star (you may want to modify this if multiple stars exist)
    main_star = stars[0]
    
    # Store the star's velocity before zeroing it
    star_velocity = main_star.vel.copy()
    
    # Zero the star's velocity and position
    main_star.vel = vec2(0, 0)
    main_star.pos = vec2(0, 0)
    
    # Adjust all planets' velocities to maintain relative motion
    for planet in planets:
        planet.vel -= star_velocity
        
    # Update camera if in star-centric mode
    if camera_mode == "star":
        update_camera_center()

def calculate_gravity():
    global particles, planets
    
    # Make copies since we'll modify the lists
    all_particles = particles.copy()
    
    for i, p1 in enumerate(all_particles):
        if p1.being_dragged:
            continue
            
        for p2 in all_particles[i+1:]:
            if p2.being_dragged:
                continue
                
            distance = (p1.pos - p2.pos).length()
            min_distance = p1.collision_radius + p2.collision_radius
            
            if distance < min_distance:
                # Star-Planet collision (existing behavior)
                if isinstance(p1, Star) and isinstance(p2, Planet):
                    handle_star_collision(p1, p2)
                elif isinstance(p2, Star) and isinstance(p1, Planet):
                    handle_star_collision(p2, p1)
                # Planet-Planet collision (new behavior)
                elif absorption_enabled and isinstance(p1, Planet) and isinstance(p2, Planet):
                    handle_planet_absorption(p1, p2)
                continue
                    
            force = Gravitational_Force(p1, p2)
            p1.apply_force(force)
            p2.apply_force(-force)

def handle_planet_absorption(planet1, planet2):
    global particles, planets
    
    # Calculate merged properties
    total_mass = planet1.mass + planet2.mass
    momentum = planet1.vel * planet1.mass + planet2.vel * planet2.mass
    
    # Calculate new radius based on selected mode
    if absorption_radius_mode == "area":
        # Radius based on combined area (πr² + πr² = πR²)
        new_radius = math.sqrt(planet1.radius**2 + planet2.radius**2)
    else:  # linear mode
        new_radius = planet1.radius + planet2.radius * 0.1  # Adjust factor as needed
    
    # Create new planet at center of mass
    com_pos = (planet1.pos * planet1.mass + planet2.pos * planet2.mass) / total_mass
    new_planet = Planet(com_pos.x, com_pos.y, total_mass, new_radius)
    new_planet.vel = momentum / total_mass
    
    # Color blending (optional)
    color1 = pygame.Color(*planet1.color)
    color2 = pygame.Color(*planet2.color)
    blend_factor = planet1.mass / total_mass
    new_color = (
        int(color1.r * blend_factor + color2.r * (1 - blend_factor)),
        int(color1.g * blend_factor + color2.g * (1 - blend_factor)),
        int(color1.b * blend_factor + color2.b * (1 - blend_factor))
    )
    new_planet.color = new_color
    
    # Remove old planets and add new one
    particles.remove(planet1)
    particles.remove(planet2)
    planets.remove(planet1)
    planets.remove(planet2)
    
    particles.append(new_planet)
    planets.append(new_planet)
    
    # Optional visual effect
    create_merge_effect(com_pos, max(planet1.radius, planet2.radius))

def create_merge_effect(position, size):
    # This could be expanded with particles or animations
    merge_circle = pygame.Surface((size*4, size*4), pygame.SRCALPHA)
    pygame.draw.circle(merge_circle, (255, 255, 100, 150), 
                      (size*2, size*2), size*2)
    screen.blit(merge_circle, world_to_screen(position) - vec2(size*2, size*2))

def handle_star_collision(star, planet):
    global particles, stars, planets
    
    # Transfer mass to star
    star.mass += planet.mass
    
    # Increase star size slightly (optional)
    star.radius = min(50, star.radius + planet.radius * 0.1)
    
    # Remove planet from all lists
    if planet in particles:
        particles.remove(planet)
    if planet in planets:
        planets.remove(planet)
        
    # # Update star color based on mass (optional visual effect)
    # mass_ratio = min(1.0, star.mass / 50)
    # star.color = (
    #     min(255, 255),
    #     max(100, 255 - int(150 * mass_ratio)),
    #     0
    # )

def is_offscreen(particle):
    screen_pos = world_to_screen(particle.pos)
    screen_width, screen_height = screen.get_size()
    margin = 100  # Extra margin beyond screen edges
    
    return (screen_pos.x < -margin or 
            screen_pos.x > screen_width + margin or
            screen_pos.y < -margin or 
            screen_pos.y > screen_height + margin)


def update_physics(dt):
    # Update physics with fixed time steps
    if paused:
        return
    calculate_gravity()
    for particle in particles:
        particle.update(dt)
    update_camera_center()

def draw_particles():
    global draw_trajectories
    # First draw all trajectories
    if draw_trajectories:
        for particle in particles:
            particle.trajectory_plot(screen, skip=5)
    
    # Then draw all particles on top
    for particle in particles:
        particle.draw(screen)

def draw_fireline():
    if planet_dragging and new_planet and drag_start_pos:
        mouse_pos = pygame.mouse.get_pos()
        start_pos = world_to_screen(drag_start_pos)
        pygame.draw.line(screen, (255, 0, 0), start_pos, mouse_pos, 2)
        pygame.draw.circle(screen, (0, 200, 200), mouse_pos, 5)
## ******************************************
##              MAIN GAME LOOP
## ******************************************
while running:
    screen.fill(background_color)
    
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
            mouse_events(event)
        if event.type == pygame.KEYDOWN:
            keypress_events(event)
    
    # Physics updates with fixed time steps
    physics_dt = delta_t * time_scale / physics_steps
    for _ in range(physics_steps):
        update_physics(physics_dt)
    
    # Drawing
    if show_grid:
        draw_grid(draw_axis=True)
        
    draw_particles()
    draw_fireline()
    # Debug info
    draw_mouse_position(screen, font)
        # Show pause indicator
    if paused:
        pause_text = font.render("PAUSED", True, (255, 255, 255))
        text_rect = pause_text.get_rect(center=(screen.get_width()//2, 20))
        screen.blit(pause_text, text_rect)
    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()

## FIX 8
## IF NO STAR, GET THE HEAVIEST BODY INSTEAD
## F2 ADD INSTRUCTION
## F3 ADD CREATION MENUE 
## BLACK HOLE CALCULATIONS
## NUCLEAR REACTOR  
## COLLISSION
## ABSORPTION