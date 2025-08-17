import pygame
import sys
import math
from typing import List, Tuple, Optional, Callable

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
BACKGROUND_COLOR = (10, 10, 10)
GRAVITY_CONSTANT = 5
GRID_COLOR = (50, 50, 50)
GRID_SPACING = 100
DEFAULT_TRAJECTORY_LENGTH = 5000
FIXED_DT = 1.0/60.0  # Fixed time step for physics (60 FPS)

# Initialize pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Partikol")
clock = pygame.time.Clock()

class State:
    """Container for position and velocity state"""
    def __init__(self, pos: pygame.math.Vector2, vel: pygame.math.Vector2):
        self.pos = pos.copy()
        self.vel = vel.copy()

class Derivative:
    """Container for velocity and acceleration derivatives"""
    def __init__(self, dpos: pygame.math.Vector2 = pygame.math.Vector2(0, 0), 
                 dvel: pygame.math.Vector2 = pygame.math.Vector2(0, 0)):
        self.dpos = dpos.copy()
        self.dvel = dvel.copy()

class CelestialBody:
    """Base class for all celestial objects."""
    def __init__(self, x: float, y: float, radius: int, color: Tuple[int, int, int], mass: float):
        self.mass = mass
        self.pos = pygame.math.Vector2(x, y)
        self.vel = pygame.math.Vector2(0, 0)
        self.acc = pygame.math.Vector2(0, 0)
        self.radius = radius
        self.collision_radius = radius
        self.color = color
        self.original_color = color
        self.dragging = False
        self.collision = False
        self.fixed = False
        self.trajectory = []
        self.true_trajectory = []
        self.prev_state = State(self.pos, self.vel)

    def apply_force(self, force: pygame.math.Vector2) -> None:
        self.acc += force / self.mass

    def acceleration(self, state: State, bodies: List['CelestialBody'], dt: float) -> pygame.math.Vector2:
        """Calculate acceleration based on current state"""
        acc = pygame.math.Vector2(0, 0)
        for body in bodies:
            if body is self or body.dragging:
                continue
            direction = body.pos - state.pos
            distance_sq = direction.length_squared()
            if distance_sq == 0:
                continue
            force_mag = GRAVITY_CONSTANT * self.mass * body.mass / distance_sq
            acc += direction.normalize() * (force_mag / self.mass)
        return acc

    def rk4_evaluate(self, state: State, bodies: List['CelestialBody'], dt: float, 
                    derivative: Derivative) -> Derivative:
        """Evaluate derivative for RK4 step"""
        new_state = State(
            state.pos + derivative.dpos * dt,
            state.vel + derivative.dvel * dt
        )
        return Derivative(
            new_state.vel,
            self.acceleration(new_state, bodies, dt)
        )

    def rk4_integrate(self, bodies: List['CelestialBody'], dt: float) -> None:
        """Perform RK4 integration step"""
        if self.fixed or self.dragging:
            return

        # Save previous state for trajectory
        self.prev_state = State(self.pos, self.vel)
        
        # RK4 integration
        initial = State(self.pos, self.vel)
        bodies_copy = [b for b in bodies if b is not self and not b.dragging]
        
        a = self.rk4_evaluate(initial, bodies_copy, 0.0, Derivative())
        b = self.rk4_evaluate(initial, bodies_copy, dt*0.5, a)
        c = self.rk4_evaluate(initial, bodies_copy, dt*0.5, b)
        d = self.rk4_evaluate(initial, bodies_copy, dt, c)
        
        dpos_dt = (a.dpos + 2.0*(b.dpos + c.dpos) + d.dpos) / 6.0
        dvel_dt = (a.dvel + 2.0*(b.dvel + c.dvel) + d.dvel) / 6.0
        
        self.pos += dpos_dt * dt
        self.vel += dvel_dt * dt
        self.acc *= 0  # Reset acceleration after integration

    def update_trajectory(self, reference_center: pygame.math.Vector2) -> None:
        """Update trajectory history for drawing."""
        self.true_trajectory.append(self.pos.copy())
        self.trajectory.append((self.pos - reference_center).copy())
        
        if len(self.trajectory) > DEFAULT_TRAJECTORY_LENGTH:
            self.trajectory.pop(0)
            self.true_trajectory.pop(0)

    def draw_trajectory(self, screen: pygame.Surface, camera_center: pygame.math.Vector2, 
                       screen_center: pygame.math.Vector2, zoom: float, 
                       color: Tuple[int, int, int], camera_mode: str, skip: int = 1) -> None:
        """Draw the object's trajectory."""
        if not self.trajectory or len(self.trajectory) < 4:
            return

        if camera_mode == "neutral":
            points = [(pos - camera_center) * zoom + screen_center 
                     for pos in self.true_trajectory[::skip]]
        else:
            points = [pos * zoom + screen_center 
                     for pos in self.trajectory[::skip]]
        
        pygame.draw.lines(screen, color, False, points, 2)

    def draw(self, screen: pygame.Surface, camera_center: pygame.math.Vector2, 
             screen_center: pygame.math.Vector2, zoom: float) -> None:
        """Draw the celestial body."""
        draw_pos = (self.pos - camera_center) * zoom + screen_center
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)

class Star(CelestialBody):
    """Star class with fixed position option."""
    def __init__(self, x: float, y: float, fixed: bool = True, 
                 radius: int = 10, color: Tuple[int, int, int] = (255, 255, 0)):
        super().__init__(x, y, radius, color, mass=50)
        self.fixed = fixed

    def update(self, bodies: List[CelestialBody], dt: float, reference_center: pygame.math.Vector2) -> None:
        if not self.fixed:
            self.rk4_integrate(bodies, dt)
        self.update_trajectory(reference_center)

class Planet(CelestialBody):
    """Planet class that orbits stars."""
    def __init__(self, x: float, y: float, radius: int = 2, 
                 color: Tuple[int, int, int] = (0, 150, 255)):
        super().__init__(x, y, radius, color, mass=1)

    def update(self, bodies: List[CelestialBody], dt: float, reference_center: pygame.math.Vector2) -> None:
        self.rk4_integrate(bodies, dt)
        self.update_trajectory(reference_center)

class Simulation:
    """Main simulation class handling all objects and physics."""
    def __init__(self):
        self.stars: List[Star] = []
        self.planets: List[Planet] = []
        self.asteroids: List[CelestialBody] = []
        self.zoom = 1.0
        self.time_scale = 60
        self.show_grid = True
        self.trajectory_plot = True
        self.camera_mode = "neutral"
        self.screen_center = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
        self.camera_center = self.screen_center.copy()
        self.current_particle: Optional[CelestialBody] = None
        self.dragging = False
        self.accumulator = 0.0
        self.remove_escapees = True

        self.right_dragging = False
        self.right_drag_start = pygame.math.Vector2(0, 0)
        self.camera_drag_start = pygame.math.Vector2(0, 0)

    
    def check_escapees(self):
        """Remove bodies exceeding escape velocity from any star"""
        if not self.remove_escapees or not self.stars:
            return
            
        for planet in self.planets[:]:  # Iterate over a copy
            for star in self.stars:
                r_vec = planet.pos - star.pos
                r = r_vec.length()
                v = planet.vel.length()
                
                # Escape velocity: sqrt(2GM/r)
                escape_vel = math.sqrt(2 * GRAVITY_CONSTANT * star.mass / r)
                
                if v > escape_vel and r > star.radius * 500:  # Safety margin
                    self.planets.remove(planet)
                    break

    def get_sphere_of_influence(self, star: Star, body: CelestialBody) -> float:
        """Calculate the sphere of influence for a star relative to another body"""
        if star is body:
            return 0
        # Simple SOI formula: a * (m/M)^(2/5)
        # Where a is semi-major axis, m is planet mass, M is star mass
        distance = star.pos.distance_to(body.pos)
        return distance * (body.mass / star.mass) ** 0.4
    
    def add_star(self, x: float, y: float, fixed: bool = False) -> None:
        """Add a new star to the simulation."""
        self.stars.append(Star(x, y, fixed))

    def add_planet(self, x: float, y: float) -> None:
        """Add a new planet to the simulation."""
        self.planets.append(Planet(x, y))

    def clear_all(self) -> None:
        """Clear all objects from the simulation."""
        self.stars = []
        self.planets = []
        self.asteroids = []

    def clear_planets(self) -> None:
        """Clear all planets from the simulation."""
        self.planets = []

    def reset_trajectories(self) -> None:
        """Clear all trajectory histories."""
        for obj in self.stars + self.planets + self.asteroids:
            obj.trajectory = []
            obj.true_trajectory = []

    def update_camera(self) -> None:
        """Update camera position based on current mode."""
        if self.camera_mode == "barycenter":
            total_mass = sum(obj.mass for obj in self.stars + self.planets)
            if total_mass > 0:
                self.camera_center = sum(
                    (obj.pos * obj.mass for obj in self.stars + self.planets),
                    pygame.math.Vector2(0, 0)
                ) / total_mass
        elif self.camera_mode == "star" and self.stars:
            self.camera_center = self.stars[0].pos

    def draw_grid(self) -> None:
        """Draw the coordinate grid."""
        if not self.show_grid:
            return

        # Compute visible area in world coordinates
        top_left = (pygame.math.Vector2(0, 0) - self.screen_center) / self.zoom + self.camera_center
        bottom_right = (pygame.math.Vector2(SCREEN_WIDTH, SCREEN_HEIGHT) - self.screen_center) / self.zoom + self.camera_center

        # Calculate grid lines to draw
        start_x = int(top_left.x // GRID_SPACING) * GRID_SPACING
        end_x = int(bottom_right.x // GRID_SPACING + 1) * GRID_SPACING
        start_y = int(top_left.y // GRID_SPACING) * GRID_SPACING
        end_y = int(bottom_right.y // GRID_SPACING + 1) * GRID_SPACING

        # Draw vertical grid lines
        for x in range(start_x, end_x, GRID_SPACING):
            start = (pygame.math.Vector2(x, start_y) - self.camera_center) * self.zoom + self.screen_center
            end = (pygame.math.Vector2(x, end_y) - self.camera_center) * self.zoom + self.screen_center
            pygame.draw.line(screen, GRID_COLOR, start, end, 1)

        # Draw horizontal grid lines
        for y in range(start_y, end_y, GRID_SPACING):
            start = (pygame.math.Vector2(start_x, y) - self.camera_center) * self.zoom + self.screen_center
            end = (pygame.math.Vector2(end_x, y) - self.camera_center) * self.zoom + self.screen_center
            pygame.draw.line(screen, GRID_COLOR, start, end, 1)

    def update_physics(self, dt: float) -> None:
        """Update all physics calculations with fixed time step."""
        reference_center = self.camera_center if self.camera_mode == "neutral" else self.get_reference_frame()
        
        # Apply forces first
        all_bodies = self.stars + self.planets + self.asteroids
        for body in all_bodies:
            body.acc *= 0  # Clear previous forces
            
        for i, body1 in enumerate(all_bodies):
            if body1.dragging:
                continue
                
            for body2 in all_bodies[i+1:]:
                if body2.dragging:
                    continue
                    
                force = body1.acceleration(State(body1.pos, body1.vel), [body2], dt)
                body1.apply_force(force)
                body2.apply_force(-force)
        
        # Then update positions with RK4
        for body in all_bodies:
            body.update(all_bodies, dt * self.time_scale, reference_center)

        self.check_escapees()

    def get_reference_frame(self) -> pygame.math.Vector2:
        """Get reference frame center based on camera mode."""
        if self.camera_mode == "barycenter":
            total_mass = sum(obj.mass for obj in self.stars + self.planets)
            if total_mass > 0:
                return sum(
                    (obj.pos * obj.mass for obj in self.stars + self.planets),
                    pygame.math.Vector2(0, 0)
                ) / total_mass
        elif self.camera_mode == "star" and self.stars:
            return self.stars[0].pos
        return pygame.math.Vector2(0, 0)

    def draw_all(self) -> None:
        """Draw all simulation elements."""
        self.draw_grid()

        # Draw trajectories
        if self.trajectory_plot:
            for planet in self.planets:
                planet.draw_trajectory(screen, self.camera_center, self.screen_center, 
                                      self.zoom, (0, 0, 200), self.camera_mode)
            for star in self.stars:
                if not star.fixed:
                    star.draw_trajectory(screen, self.camera_center, self.screen_center, 
                                        self.zoom, (200, 200, 0), self.camera_mode)

        # Draw celestial bodies
        for planet in self.planets:
            planet.draw(screen, self.camera_center, self.screen_center, self.zoom)
        for star in self.stars:
            star.draw(screen, self.camera_center, self.screen_center, self.zoom)

        # Draw drag line if dragging
        if self.dragging and self.current_particle:
            mouse_pos = pygame.mouse.get_pos()
            pygame.draw.line(
                screen, (255, 0, 0),
                (self.current_particle.pos - self.camera_center) * self.zoom + self.screen_center,
                mouse_pos, 2
            )
            pygame.draw.circle(screen, (0, 200, 200), mouse_pos, 2)

        
        display_font = pygame.font.SysFont("Consolas", 15)
        # Display time scale
        time_text = display_font.render(f"Time Scale: {self.time_scale / 60}x", True, (255, 255, 255))
        screen.blit(time_text, (10, 10))
        # Display time scale
        zoom_text = display_font.render(f"Zoom Scale: {self.zoom:.3f}x", True, (255, 255, 255))
        screen.blit(zoom_text, (10, 30))
        # Display escapees mode status
        esc_text = display_font.render(
            f"Remove Escapees: {'ON' if self.remove_escapees else 'OFF'}", 
            True, 
            (0, 255, 0) if self.remove_escapees else (255, 0, 0)
        )
        screen.blit(esc_text, (10, 50))
        # Display mouse world and screen position
        mouse_pos = pygame.mouse.get_pos()
        world_pos = (pygame.math.Vector2(mouse_pos) - self.screen_center) / self.zoom + self.camera_center
        mouse_pos_screen = display_font.render(f"Screen Pos : {mouse_pos}", True, (255, 255, 255))
        mouse_pos_world  = display_font.render(f"World  Pos : {world_pos}", True, (255, 255, 255))
        screen.blit(mouse_pos_screen, (10, SCREEN_HEIGHT-20))
        screen.blit(mouse_pos_world, (10, SCREEN_HEIGHT-40))
        
    def handle_events(self) -> bool:
        """Handle pygame events. Returns False if simulation should quit."""
        mouse_pos = pygame.mouse.get_pos()
        world_pos = (pygame.math.Vector2(mouse_pos) - self.screen_center) / self.zoom + self.camera_center

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            # Handle mouse events
            if event.type in (pygame.MOUSEBUTTONDOWN, pygame.MOUSEBUTTONUP, pygame.MOUSEMOTION):
                self.handle_mouse_events(event)

            # Handle keyboard events
            if event.type == pygame.KEYDOWN:
                self.handle_keydown(event, world_pos)
            elif event.type == pygame.KEYUP and event.key == pygame.K_f and self.current_particle and self.dragging:
                self.handle_drag_release(mouse_pos)

        return True
    
    def handle_mouse_events(self, event: pygame.event.Event) -> None:
        """Handle all mouse-related events."""
        mouse_pos = pygame.mouse.get_pos()
        world_pos = (pygame.math.Vector2(mouse_pos) - self.screen_center) / self.zoom + self.camera_center

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 3:  # Right mouse button
                self.right_dragging = True
                self.right_drag_start = pygame.math.Vector2(mouse_pos)
                self.camera_drag_start = self.camera_center.copy()
            elif event.button == 4:  # Scroll up - zoom in
                self.zoom *= 1.1
            elif event.button == 5:  # Scroll down - zoom out
                self.zoom /= 1.1
            # elif event.button == 1:  # Left click - selection (if you want to add it later)
            #     pass

        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 3:  # Right mouse button
                self.right_dragging = False

        elif event.type == pygame.MOUSEMOTION:
            if self.right_dragging:
                mouse_delta = (pygame.math.Vector2(mouse_pos) - self.right_drag_start) / self.zoom
                self.camera_center = self.camera_drag_start - mouse_delta

    def handle_keydown(self, event: pygame.event.Event, world_pos: pygame.math.Vector2) -> None:
        """Handle keyboard input using match-case."""
        match event.key:
            case pygame.K_e:  # Toggle escapee removal
                self.remove_escapees = not self.remove_escapees
            case pygame.K_BACKSPACE:  # Clear all objects
                self.clear_all()
            case pygame.K_g:  # Toggle grid
                self.show_grid = not self.show_grid
            case pygame.K_p:  # Clear planets
                self.clear_planets()
            case pygame.K_s:  # Add star
                self.add_star(world_pos.x, world_pos.y, False)
            case pygame.K_t:  # Toggle trajectory plot
                self.trajectory_plot = not self.trajectory_plot
            case pygame.K_EQUALS:  # Zoom in
                self.zoom *= 1.1
            case pygame.K_MINUS:  # Zoom out
                self.zoom /= 1.1
            case pygame.K_r:  # Reset trajectories
                self.reset_trajectories()
            case pygame.K_b:  # Barycenter camera mode
                self.camera_mode = "barycenter"
                self.reset_trajectories()
            case pygame.K_m:  # Star camera mode
                self.camera_mode = "star"
                self.reset_trajectories()
            case pygame.K_n:  # Neutral camera mode
                self.camera_mode = "neutral"
                self.reset_trajectories()
            case pygame.K_COMMA:  # Decrease time scale
                self.time_scale /= 2
            case pygame.K_PERIOD:  # Increase time scale
                self.time_scale *= 2
            case pygame.K_0:  # Reset view
                self.zoom = 1
                self.camera_center = pygame.math.Vector2(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
            case pygame.K_f:  # Start drag
                self.handle_drag_start(world_pos)
            case pygame.K_c:  # Create orbiting planet
                self.create_orbiting_planet(world_pos)
            case pygame.K_LEFT | pygame.K_RIGHT | pygame.K_UP | pygame.K_DOWN:  # Camera movement
                self.handle_camera_movement(event.key)
            case _:  # Default case (no action)
                pass

    def handle_camera_movement(self, key: int) -> None:
        """Handle camera movement with arrow keys."""
        shift = SCREEN_WIDTH / 32 / self.zoom  # make shift size zoom-independent
        if key == pygame.K_LEFT:
            self.camera_center.x -= shift
        elif key == pygame.K_RIGHT:
            self.camera_center.x += shift
        elif key == pygame.K_UP:
            self.camera_center.y -= shift
        elif key == pygame.K_DOWN:
            self.camera_center.y += shift

    def handle_drag_start(self, world_pos: pygame.math.Vector2) -> None:
        """Start dragging a new planet."""
        p = Planet(world_pos.x, world_pos.y)
        p.dragging = True
        self.current_particle = p
        self.dragging = True
        self.planets.append(p)

    def handle_drag_release(self, mouse_pos: Tuple[int, int]) -> None:
        """Release a dragged planet and set its velocity."""
        if not self.current_particle:
            return

        world_pos = (pygame.math.Vector2(mouse_pos) - self.screen_center) / self.zoom + self.camera_center
        drag_vector = self.current_particle.pos - pygame.Vector2(world_pos)
        self.current_particle.vel = drag_vector * 0.05
        self.current_particle.dragging = False
        self.current_particle = None
        self.dragging = False

    def create_orbiting_planet(self, world_pos: pygame.math.Vector2) -> None:
        """Create a planet in circular orbit around nearest star."""
        if not self.stars:
            return

        # Find closest star to mouse position
        closest_star = min(self.stars, key=lambda s: (s.pos - world_pos).length_squared())
        r_vec = world_pos - closest_star.pos
        r = r_vec.length()

        if r == 0:
            return  # avoid division by zero

        # Calculate orbital velocity
        radial_dir = r_vec.normalize()
        perpendicular = pygame.math.Vector2(-radial_dir.y, radial_dir.x)  # CCW by default
        
        # Determine direction based on cross product
        if closest_star.pos.cross(world_pos) < 0:
            perpendicular *= -1  # flip to CW

        v_mag = math.sqrt(GRAVITY_CONSTANT * closest_star.mass / r)

        # Create orbiting planet
        new_planet = Planet(world_pos.x, world_pos.y)
        new_planet.vel = perpendicular * v_mag
        self.planets.append(new_planet)

def main():
    """Main game loop with fixed time step physics."""
    sim = Simulation()
    running = True
    prev_time = pygame.time.get_ticks() / 1000.0
    
    while running:
        current_time = pygame.time.get_ticks() / 1000.0
        frame_time = current_time - prev_time
        prev_time = current_time
        
        # Cap frame time to avoid spiral of death
        frame_time = min(frame_time, 0.25)
        
        # Fixed time step physics
        sim.accumulator += frame_time
        while sim.accumulator >= FIXED_DT:
            sim.update_physics(FIXED_DT)
            sim.accumulator -= FIXED_DT
        
        screen.fill(BACKGROUND_COLOR)
        
        # Update camera and handle input
        sim.update_camera()
        running = sim.handle_events()
        sim.draw_all()
        
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

## F2 ADD INSTRUCTION
## F3 ADD CREATION MENUE 
## BLACK HOLE CALCULATIONS
## COLLISSION
## ABSORPTION