import pygame
from settings import FPS, WIDTH, HEIGHT, GRAVITY, COLORS

PARTICLE_RADIUS = 10
SPACING = 50
GRID_X, GRID_Y = 10, 10


class Particle:
    def __init__(self, position, fixed=False):
        self.position = pygame.Vector2(position)
        self.previous_position = self.position.copy()
        self.fixed = fixed
        self.selected = False

    def update(self, delta_time):
        if self.fixed or self.selected:
            return
        # Verlet integration: x_new = x + (x - x_prev) + a * dt^2
        self.previous_position = self.position.copy()
        self.position += pygame.Vector2(0, GRAVITY) * delta_time * delta_time

    def draw(self, surface):
        color = COLORS['red'] if self.selected else COLORS['white']
        pygame.draw.circle(surface, color, self.position, PARTICLE_RADIUS)


class Constraint:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.rest_length = a.position.distance_to(b.position)

    def update(self):

        # Position-Based Dynamics
        diff = self.b.position - self.a.position
        dist = diff.length()
        if dist == 0:
            return
        direction = diff / dist
        offset = (dist - self.rest_length) / 2
        adjustment = direction * offset
        if not self.a.fixed:
            self.a.position += adjustment
        if not self.b.fixed:
            self.b.position -= adjustment

    def draw(self, surface):
        pygame.draw.line(surface, COLORS['white'], self.a.position, self.b.position, 1)


def create_particles():
    particles = []
    start_x = (WIDTH - (GRID_X - 1) * SPACING) / 2
    start_y = (HEIGHT - (GRID_Y - 1) * SPACING) / 2
    for y in range(GRID_Y):
        for x in range(GRID_X):
            position = (start_x + x * SPACING, start_y + y * SPACING)
            fixed = (x in (0, GRID_X - 1) and y in (0, GRID_Y - 1))
            particles.append(Particle(position, fixed))
    return particles


def create_constraints(particles):
    constraints = []
    idx = lambda x, y: x + y * GRID_X
    for y in range(GRID_Y):
        for x in range(GRID_X):
            p = particles[idx(x, y)]
            if x < GRID_X - 1:
                constraints.append(Constraint(p, particles[idx(x + 1, y)]))
            if y < GRID_Y - 1:
                constraints.append(Constraint(p, particles[idx(x, y + 1)]))
            if x < GRID_X - 1 and y < GRID_Y - 1:
                constraints.append(Constraint(p, particles[idx(x + 1, y + 1)]))
                constraints.append(Constraint(particles[idx(x + 1, y)], particles[idx(x, y + 1)]))
    return constraints


def find_nearest(particles, mouse_position):
    for particle in particles:
        if (particle.position - mouse_position).length_squared() < 300:
            particle.selected = True
            return particle
    return None


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    particles = create_particles()
    constraints = create_constraints(particles)
    selected = None

    running = True
    while running:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                selected = find_nearest(particles, pygame.Vector2(pygame.mouse.get_pos()))
            elif event.type == pygame.MOUSEBUTTONUP:
                if selected:
                    selected.selected = False
                selected = None

        if selected:
            selected.position = pygame.Vector2(pygame.mouse.get_pos())

        for particle in particles:
            particle.update(delta_time)
        for _ in range(5):
            for constraint in constraints:
                constraint.update()

        screen.fill(COLORS['black'])
        for constraint in constraints:
            constraint.draw(screen)
        for particle in particles:
            particle.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
