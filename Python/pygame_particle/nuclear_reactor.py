# Updated simulation code with the requested features:
# - Uranium in a square of side length `n`
# - Distance between uraniums is configurable ("density")
# - Speed variation for neutrons
# - Neutrons skip uranium when fast
# - Gamma rays cause motion of uranium
# - Uranium removed upon fission
# - Reflective wall toggle
# - Friction and decay for uranium motion
# - Energy increases when gamma hits wall

import pygame
import sys
import random
import math
import numpy as np
from collections import deque

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
FPS = 60
BACKGROUND_COLOR = (0, 0, 0)
WALL_COLOR = (100, 100, 100)
REACTOR_COLOR = (50, 50, 50)

# Particle colors
NEUTRON_COLOR = (255, 255, 0)
URANIUM_COLOR = (0, 255, 0)
GAMMA_COLOR = (255, 255, 255)
PRODUCT_COLOR = (150, 150, 150)

# Physics parameters
NEUTRON_BASE_SPEED = 5
NEUTRON_SPEED_VARIATION = 3
GAMMA_SPEED = 10
FISSION_ENERGY = 50
THERMAL_NEUTRON_THRESHOLD = 12
FISSION_NEUTRON_RANGE = (2, 3)
FISSION_PROBABILITY = 1

URANIUM_GRID_N = 10        # Square root of uranium atoms count
URANIUM_SPACING = 10        # Distance between uranium atoms
URANIUM_RADIUS = 5
FRICTION = 0.99

REFLECTIVE_WALLS = False

# Energy graph
GRAPH_WIDTH = 400
GRAPH_HEIGHT = 80
GRAPH_POS = (100, 500)
MAX_ENERGY_HISTORY = 100

class Particle:
    def __init__(self, x, y, vx, vy, radius, color, lifetime=float('inf')):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.radius = radius
        self.color = color
        self.lifetime = lifetime
        self.age = 0

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.age += 1

        if isinstance(self, (GammaRay, Neutron)):
            return

        self.vx *= FRICTION
        self.vy *= FRICTION

        # Bounce off walls
        if self.x - self.radius < 0 or self.x + self.radius > WIDTH:
            self.vx *= -1
            self.x = max(self.radius, min(WIDTH - self.radius, self.x))
        if self.y - self.radius < 0 or self.y + self.radius > HEIGHT:
            self.vy *= -1
            self.y = max(self.radius, min(HEIGHT - self.radius, self.y))

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def is_dead(self):
        return (self.age >= self.lifetime or 
                self.x < -self.radius or self.x > WIDTH + self.radius or
                self.y < -self.radius or self.y > HEIGHT + self.radius)

class Neutron(Particle):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy, 2, NEUTRON_COLOR, 1000)
    
    def speed(self):
        return math.hypot(self.vx, self.vy)

    def is_thermal(self):
        return self.speed() < THERMAL_NEUTRON_THRESHOLD

class Uranium(Particle):
    def __init__(self, x, y):
        super().__init__(x, y, 0, 0, URANIUM_RADIUS, URANIUM_COLOR)
        self.fissionable = random.random() < FISSION_PROBABILITY

class GammaRay(Particle):
    def __init__(self, x, y, vx, vy):
        super().__init__(x, y, vx, vy, 1, GAMMA_COLOR, 300)

class ProductNucleus(Particle):
    def __init__(self, x, y):
        vx = random.uniform(-2, 2)
        vy = random.uniform(-2, 2)
        super().__init__(x, y, vx, vy, 4, PRODUCT_COLOR, 500)

class ReactorSimulation:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Nuclear Reactor Simulation")
        self.clock = pygame.time.Clock()
        self.particles = []
        self.energy_history = deque(maxlen=MAX_ENERGY_HISTORY)
        self.total_energy = 0
        # self.setup_uranium_square()
        self.setup_uranium_circle()

    def setup_uranium_circle(self):
        center_x, center_y = WIDTH // 2, HEIGHT // 2
        radius = (URANIUM_GRID_N - 1) * URANIUM_SPACING / 2

        for i in range(URANIUM_GRID_N):
            for j in range(URANIUM_GRID_N):
                x = i * URANIUM_SPACING - radius
                y = j * URANIUM_SPACING - radius
                dist = math.hypot(x, y)

                if dist <= radius:
                    self.particles.append(Uranium(center_x + x, center_y + y))

    def setup_uranium_square(self):
        margin_x = (WIDTH - (URANIUM_GRID_N - 1) * URANIUM_SPACING) // 2
        margin_y = (HEIGHT - (URANIUM_GRID_N - 1) * URANIUM_SPACING) // 2
        for i in range(URANIUM_GRID_N):
            for j in range(URANIUM_GRID_N):
                x = margin_x + i * URANIUM_SPACING
                y = margin_y + j * URANIUM_SPACING
                self.particles.append(Uranium(x, y))

    def add_neutron(self, x=None, y=None):
        if x is None:
            x = random.randint(0, WIDTH)
        if y is None:
            y = random.randint(0, HEIGHT)
        angle = random.uniform(0, 2 * math.pi)
        speed = NEUTRON_BASE_SPEED + random.uniform(-NEUTRON_SPEED_VARIATION, NEUTRON_SPEED_VARIATION)
        vx = speed * math.cos(angle)
        vy = speed * math.sin(angle)
        self.particles.append(Neutron(x, y, vx, vy))

    def check_collisions(self):
        neutrons = [p for p in self.particles if isinstance(p, Neutron)]
        uraniums = [p for p in self.particles if isinstance(p, Uranium)]
        gammas = [p for p in self.particles if isinstance(p, GammaRay)]
        
        uraniums_to_remove = set()

        # Gamma ray interactions
        for gamma in gammas:
            for atom in uraniums:
                dx, dy = gamma.x - atom.x, gamma.y - atom.y
                if math.hypot(dx, dy) < gamma.radius + atom.radius:
                    atom.vx += dx * 0.05
                    atom.vy += dy * 0.05

        # Neutron collisions and fission
        for neutron in neutrons:
            for atom in uraniums:
                if atom in uraniums_to_remove:
                    continue  # Already scheduled for removal
                
                dx, dy = neutron.x - atom.x, neutron.y - atom.y
                if math.hypot(dx, dy) < neutron.radius + atom.radius:
                    if neutron.is_thermal() and atom.fissionable:
                        self.total_energy += FISSION_ENERGY
                        uraniums_to_remove.add(atom)

                        self.particles.append(ProductNucleus(atom.x, atom.y))
                        self.particles.append(ProductNucleus(atom.x, atom.y))

                        for _ in range(4):
                            angle = random.uniform(0, 2 * math.pi)
                            self.particles.append(GammaRay(atom.x, atom.y,
                                                        GAMMA_SPEED * math.cos(angle),
                                                        GAMMA_SPEED * math.sin(angle)))

                        for _ in range(random.randint(*FISSION_NEUTRON_RANGE)):
                            angle = random.uniform(0, 2 * math.pi)
                            speed = NEUTRON_BASE_SPEED + random.uniform(-NEUTRON_SPEED_VARIATION, NEUTRON_SPEED_VARIATION)
                            self.particles.append(Neutron(atom.x, atom.y,
                                                        speed * math.cos(angle),
                                                        speed * math.sin(angle)))
                    break  # stop checking this neutron

        for atom in uraniums_to_remove:
            if atom in self.particles:
                self.particles.remove(atom)


    def update(self):
        for p in self.particles[:]:
            p.update()
            if p.is_dead():
                self.particles.remove(p)

        self.check_collisions()

        # Reflective wall gamma bounce and energy
        if REFLECTIVE_WALLS:
            for p in self.particles:
                if isinstance(p, GammaRay):
                    bounced = False
                    if p.x - p.radius < 0 or p.x + p.radius > WIDTH:
                        p.vx *= -1
                        bounced = True
                    if p.y - p.radius < 0 or p.y + p.radius > HEIGHT:
                        p.vy *= -1
                        bounced = True
                    if bounced:
                        self.total_energy += 1

        self.energy_history.append(self.total_energy)
        self.total_energy *= 1

    def draw_energy_graph(self):
        if len(self.energy_history) < 2:
            return
        max_energy = max(self.energy_history) or 1
        points = [(GRAPH_POS[0] + i / (MAX_ENERGY_HISTORY - 1) * GRAPH_WIDTH,
                   GRAPH_POS[1] + GRAPH_HEIGHT - e / max_energy * GRAPH_HEIGHT)
                  for i, e in enumerate(self.energy_history)]
        pygame.draw.lines(self.screen, (255, 255, 255), False, points, 2)
        pygame.draw.rect(self.screen, (255, 255, 255),
                         (*GRAPH_POS, GRAPH_WIDTH, GRAPH_HEIGHT), 1)

    def draw(self):
        self.screen.fill(BACKGROUND_COLOR)
        pygame.draw.rect(self.screen, REACTOR_COLOR, (0, 0, WIDTH, HEIGHT), 2)
        for p in self.particles:
            p.draw(self.screen)
        self.draw_energy_graph()
        font = pygame.font.SysFont(None, 24)
        stats = f"Particles: {len(self.particles)} | Energy: {int(self.total_energy)}"
        self.screen.blit(font.render(stats, True, (255, 255, 255)), (10, 10))
        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.add_neutron(*event.pos)
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        for _ in range(5):
                            self.add_neutron()
                    elif event.key == pygame.K_r:
                        global REFLECTIVE_WALLS
                        REFLECTIVE_WALLS = not REFLECTIVE_WALLS

            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    ReactorSimulation().run()
