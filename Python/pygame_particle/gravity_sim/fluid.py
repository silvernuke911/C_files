import pygame
import numpy as np
import matplotlib.cm as cm

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 200, 200
SCALE = 2  # Scale up for display
DT = 0.4  # Time step
DIFFUSION = 0.0001  # Density diffusion rate
VISCOSITY = 0.0001  # Velocity diffusion rate
ITERATIONS = 4  # For pressure solver

# Create a grid
N = WIDTH
size = (N, N)
density = np.zeros(size)
velocity_x = np.zeros(size)
velocity_y = np.zeros(size)

# Initialize display
screen = pygame.display.set_mode((WIDTH * SCALE, HEIGHT * SCALE))
pygame.display.set_caption("2D Fluid Simulation")
clock = pygame.time.Clock()

# Inferno colormap
inferno = cm.get_cmap('inferno')

def add_density(x, y, amount=100):
    """Add density at a point (e.g., mouse position)"""
    if 0 <= x < N and 0 <= y < N:
        density[x, y] += amount

def add_velocity(x, y, dx, dy):
    """Add velocity at a point"""
    if 0 <= x < N and 0 <= y < N:
        velocity_x[x, y] += dx
        velocity_y[x, y] += dy

def step():
    """Update fluid simulation"""
    global velocity_x, velocity_y, density

    # Diffuse velocity and density
    velocity_x = diffuse(velocity_x, VISCOSITY)
    velocity_y = diffuse(velocity_y, VISCOSITY)
    density = diffuse(density, DIFFUSION)

    # Project to ensure incompressibility
    project(velocity_x, velocity_y)

    # Advect density and velocity
    velocity_x, velocity_y = advect(velocity_x, velocity_y, velocity_x, velocity_y)
    density = advect(density, velocity_x, velocity_y)

    # Project again
    project(velocity_x, velocity_y)

# --- Core Fluid Simulation Functions ---
def diffuse(field, rate):
    """Diffuse a field (density or velocity)"""
    new_field = field.copy()
    for _ in range(ITERATIONS):
        new_field[1:-1, 1:-1] = (
            field[1:-1, 1:-1] + 
            rate * (
                new_field[:-2, 1:-1] + 
                new_field[2:, 1:-1] + 
                new_field[1:-1, :-2] + 
                new_field[1:-1, 2:]
            )
        ) / (1 + 4 * rate)
    return new_field

def advect(field, vel_x, vel_y):
    """Advect a field (density or velocity)"""
    new_field = np.zeros_like(field)
    for i in range(1, N-1):
        for j in range(1, N-1):
            # Trace particle backward in time
            x = i - vel_x[i, j] * DT
            y = j - vel_y[i, j] * DT
            x = max(0.5, min(N-1.5, x))
            y = max(0.5, min(N-1.5, y))

            # Bilinear interpolation
            x0, y0 = int(x), int(y)
            x1, y1 = x0 + 1, y0 + 1
            s1, s0 = x - x0, y - y0
            t1, t0 = 1 - s1, 1 - s0

            new_field[i, j] = (
                t0 * (t1 * field[x0, y0] + s1 * field[x1, y0]) +
                s0 * (t1 * field[x0, y1] + s1 * field[x1, y1])
            )
    return new_field

def project(vel_x, vel_y):
    """Project velocity field to be divergence-free"""
    divergence = np.zeros(size)
    pressure = np.zeros(size)

    # Compute divergence
    divergence[1:-1, 1:-1] = (
        (vel_x[2:, 1:-1] - vel_x[:-2, 1:-1]) + 
        (vel_y[1:-1, 2:] - vel_y[1:-1, :-2])
    ) * -0.5

    # Solve pressure (simplified)
    for _ in range(ITERATIONS):
        pressure[1:-1, 1:-1] = (
            divergence[1:-1, 1:-1] + 
            pressure[:-2, 1:-1] + 
            pressure[2:, 1:-1] + 
            pressure[1:-1, :-2] + 
            pressure[1:-1, 2:]
        ) / 4

    # Subtract pressure gradient
    vel_x[1:-1, 1:-1] -= (pressure[2:, 1:-1] - pressure[:-2, 1:-1]) * 0.5
    vel_y[1:-1, 1:-1] -= (pressure[1:-1, 2:] - pressure[1:-1, :-2]) * 0.5

# --- Main Loop ---
running = True
mouse_down = False

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_down = False

    if mouse_down:
        mx, my = pygame.mouse.get_pos()
        mx //= SCALE
        my //= SCALE
        add_density(mx, my, 100)
        add_velocity(mx, my, np.random.uniform(-1, 1), np.random.uniform(-1, 1))

    # Update simulation
    step()

    # Render
    screen.fill((0, 0, 0))
    norm_density = np.clip(density / 100, 0, 1)  # Normalize for colormap
    for i in range(N):
        for j in range(N):
            color = inferno(norm_density[i, j])  # Apply inferno colormap
            pygame.draw.rect(
                screen, 
                (color[0] * 255, color[1] * 255, color[2] * 255), 
                (i * SCALE, j * SCALE, SCALE, SCALE)
            )

    pygame.display.flip()
    clock.tick(30)

pygame.quit()