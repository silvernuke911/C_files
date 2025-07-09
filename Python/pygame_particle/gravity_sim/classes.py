import pygame 

class Particle():
    def __init__(self, x ,y , mass, radius, color):
        self.mass = mass 
        self.pos = pygame.math.Vector2(x,y)
        self.vel = pygame.math.Vector2(x,y)
        self.acc = pygame.math.Vector2(x,y)
        self.radius = radius 
        self.collision_radius = radius
        self.color = color 
        self.dragging = False
        self.collision = False
        self.fixed = False
        self.true_trajectory = []
        self.camera_trajectory = []
    
    def apply_force(self, force):
        self.acc += force / self.mass

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
            self.vel += self.acc 
            self.pos += self.vel 
        self.acc *= 0
        self.true_trajectory.append(self.pos.copy())
        # reference_center = functions.get_reference_frame(camera_mode)
        #self.trajectory.append((self.pos - reference_center).copy())
        # if len(self.trajectory) > 5000:
        #     self.trajectory.pop(0)

    def trajectory_plot(self, screen, camera_mode, camera_center, screen_center, zoom, skip=1):
        if camera_mode == "neutral":
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos - camera_center) * zoom + screen_center
                    for pos in self.true_trajectory[::skip]
                ]
                pygame.draw.lines(screen, self.color * 0.75, False, transformed_trajectory, 2)
        else:
            if len(self.trajectory) >= 4:
                transformed_trajectory = [
                    (pos) * zoom + screen_center
                    for pos in self.trajectory[::skip]
                ]
                pygame.draw.lines(screen, self.color * 0.75, False, transformed_trajectory, 2)
    def draw(self, screen):
        global zoom
        draw_pos = world_to_screen(self.pos)
        draw_radius = max(1, int(self.radius * zoom))
        pygame.draw.circle(screen, self.color, draw_pos, draw_radius)



class Star(Particle):
    def __init__(self, x, y, mass = 20, radius = 10, color = (255,0,0)):
        super().__init__(x, y, mass, radius, color)

    def apply_force(self, force):
        super().apply_force(force)

    def update(self, camera_mode):
        super().update(camera_mode)

    def trajectory_plot(self, screen, camera_mode, camera_center, screen_center, zoom, skip=1):
        super().trajectory_plot(screen, camera_mode, camera_center, screen_center, zoom, skip)

    def draw(self, screen):
        super().draw(screen)


class Planet(Particle):
    def __init__(self, x, y, mass = 1, radius = 2, color = (0,0,255)):
        super().__init__(x, y, mass, radius, color)

    def apply_force(self, force):
        super().apply_force(force)

    def update(self, camera_mode):
        super().update(camera_mode)

    def trajectory_plot(self, screen, camera_mode, camera_center, screen_center, zoom, skip=1):
        super().trajectory_plot(screen, camera_mode, camera_center, screen_center, zoom, skip)

    def draw(self, screen):
        super().draw(screen)


class ParticleC(Particle):
    def __init__(self, x, y, mass = 0, radius = 1, color = (200,200,200)):
        super().__init__(x, y, mass, radius, color)

    def apply_force(self, force):
        super().apply_force(force)

    def update(self, camera_mode):
        super().update(camera_mode)

    def trajectory_plot(self, screen, camera_mode, camera_center, screen_center, zoom, skip=1):
        super().trajectory_plot(screen, skip)

    def draw(self, screen):
        super().draw(screen)
