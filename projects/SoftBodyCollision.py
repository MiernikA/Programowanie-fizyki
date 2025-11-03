import pygame
import pygame_gui
import math
from settings import FPS, WIDTH, HEIGHT, GRAVITY, COLORS

FLOOR_Y = 850
POINT_RADIUS = 8


class Point:
    def __init__(self, x, y, mass=1):
        self.position = pygame.Vector2(x, y)
        self.velocity = pygame.Vector2()
        self.force = pygame.Vector2()
        self.mass = mass

    def apply_force(self, force):
        self.force += force

    def update(self, delta_time):
        acceleration = self.force / self.mass
        self.velocity += acceleration * delta_time
        self.position += self.velocity * delta_time
        self.force = pygame.Vector2()


class Spring:
    def __init__(self, a, b, rest_length, stiffness, damping=0.1):
        self.a = a
        self.b = b
        self.rest_length = rest_length
        self.stiffness = stiffness
        self.damping = damping

    def apply(self):
        diff = self.b.position - self.a.position
        current_length = diff.length()
        if current_length == 0:
            return
        direction = diff / current_length
        spring_force = self.stiffness * (current_length - self.rest_length)
        relative_velocity = (self.b.velocity - self.a.velocity).dot(direction)
        damping_force = self.damping * relative_velocity
        total_force = (spring_force + damping_force) * direction
        self.a.apply_force(total_force)
        self.b.apply_force(-total_force)


class SoftBody:
    def __init__(self, center, radius, point_count, stiffness_perimeter, stiffness_center, damping):
        self.points = []
        self.springs = []

        center_point = Point(*center)
        self.points.append(center_point)

        angle_step = 2 * math.pi / point_count
        for i in range(point_count):
            angle = i * angle_step
            x = center[0] + radius * math.cos(angle)
            y = center[1] + radius * math.sin(angle)
            self.points.append(Point(x, y))

        for i in range(1, point_count + 1):
            self.springs.append(Spring(center_point, self.points[i], radius, stiffness_center, damping))

        edge_length = 2 * radius * math.sin(math.pi / point_count)
        for i in range(1, point_count + 1):
            a = self.points[i]
            b = self.points[1 + (i % point_count)]
            self.springs.append(Spring(a, b, edge_length, stiffness_perimeter, damping))

    def update(self, delta_time):
        for spring in self.springs:
            spring.apply()

        for point in self.points:
            point.apply_force(pygame.Vector2(0, GRAVITY * point.mass * 20))
            point.update(delta_time)

        for point in self.points:
            if point.position.y > FLOOR_Y:
                point.position.y = FLOOR_Y
                if point.velocity.y > 0:
                    point.velocity.y *= -0.4
                    point.velocity.x *= 0.9

    def draw(self, surface):
        for spring in self.springs:
            pygame.draw.line(surface, COLORS['blue'], spring.a.position, spring.b.position, 2)
        for point in self.points:
            pygame.draw.circle(surface, COLORS['red'], point.position, POINT_RADIUS)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    manager = pygame_gui.UIManager((WIDTH, HEIGHT))
    font = pygame.font.SysFont(None, 30)

    slider = pygame_gui.elements.UIHorizontalSlider(
        relative_rect=pygame.Rect((WIDTH // 2 - 275, 20), (300, 30)),
        start_value=3,
        value_range=(3, 30),
        manager=manager
    )
    reset_button = pygame_gui.elements.UIButton(
        relative_rect=pygame.Rect((WIDTH // 2 + 35, 15), (100, 40)),
        text='RESET',
        manager=manager
    )

    def create_body():
        return SoftBody(
            center=(WIDTH // 2, 200),
            radius=100,
            point_count=int(slider.get_current_value()),
            stiffness_perimeter=800,
            stiffness_center=500,
            damping=1.0
        )

    body = create_body()
    running = True

    while running:
        delta_time = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == reset_button:
                body = create_body()
            manager.process_events(event)

        manager.update(delta_time)
        body.update(delta_time)

        screen.fill(COLORS['black'])
        pygame.draw.rect(screen, COLORS['grey'], (0, FLOOR_Y, WIDTH, HEIGHT - FLOOR_Y))
        body.draw(screen)
        manager.draw_ui(screen)

        text_surface = font.render(f'POINTS: {int(slider.get_current_value())}', True, COLORS['white'])
        screen.blit(text_surface, (WIDTH // 2 + 160, 25))

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
