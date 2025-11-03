import pygame
import random

from settings import (
    FPS,
    WIDTH, HEIGHT,
    GRAVITY,
    COLORS
)

CIRCLE_CENTER = pygame.Vector2(WIDTH / 2, HEIGHT / 2)
CIRCLE_RADIUS = 300
BALL_RADIUS = 15


class Ball:

    def __init__(self, position, velocity):
        self.position = pygame.Vector2(position)
        self.velocity = pygame.Vector2(velocity)
        self.color = random.choice([COLORS['red'], COLORS['blue']])

    def next_color(self):
        return COLORS['blue'] if self.color == COLORS['red'] else COLORS['red']

    def update(self, delta_time):
        # accelerated motion -> v = v0 + a * dt
        self.velocity.y += GRAVITY * delta_time
        self.position += self.velocity * delta_time

        to_center_vector = self.position - CIRCLE_CENTER
        distance_to_center = to_center_vector.length()
        if distance_to_center + BALL_RADIUS > CIRCLE_RADIUS:
            normal_vector = to_center_vector.normalize()
            self.position = CIRCLE_CENTER + normal_vector * (CIRCLE_RADIUS - BALL_RADIUS)

            # Elastic rebound
            # v' = v - 2 (v·n) n
            self.velocity -= 2 * self.velocity.dot(normal_vector) * normal_vector
            self.color = self.next_color()

    def draw(self, surface):
        pygame.draw.circle(
            surface,
            self.color,
            (int(self.position.x), int(self.position.y)),
            BALL_RADIUS
        )


def create_balls():
    balls = []
    for _ in range(10):
        while True:
            position = CIRCLE_CENTER + pygame.Vector2(
                random.uniform(-CIRCLE_RADIUS / 2, CIRCLE_RADIUS / 2),
                random.uniform(-CIRCLE_RADIUS / 2, CIRCLE_RADIUS / 2)
            )
            if (position - CIRCLE_CENTER).length() + BALL_RADIUS < CIRCLE_RADIUS:
                break
        velocity = pygame.Vector2(
            random.uniform(-2, 2),
            random.uniform(-2, 2)
        )
        balls.append(Ball(position, velocity))
    return balls


def handle_ball_collisions(balls):
    for i in range(len(balls)):
        for j in range(i + 1, len(balls)):
            ball_a, ball_b = balls[i], balls[j]
            delta_vector = ball_b.position - ball_a.position
            distance = delta_vector.length()
            if 0 < distance < 2 * BALL_RADIUS:
                normal_vector = delta_vector / distance
                overlap = 2 * BALL_RADIUS - distance
                ball_a.position -= normal_vector * (overlap / 2)
                ball_b.position += normal_vector * (overlap / 2)

                # --- Elastic rebound ---

                # v1' = v1 - (v1 - v2)·n * n
                # v2' = v2 + (v1 - v2)·n * n

                relative_velocity = ball_a.velocity - ball_b.velocity
                impulse = 2 * relative_velocity.dot(normal_vector) / 2
                ball_a.velocity -= impulse * normal_vector
                ball_b.velocity += impulse * normal_vector

                ball_a.color = ball_a.next_color()
                ball_b.color = ball_b.next_color()


def main():
    pygame.init()
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    balls = create_balls()
    running = True

    while running:
        delta_time = clock.tick(FPS) / 100.0  # Gravity * 100

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for ball in balls:
            ball.update(delta_time)
        handle_ball_collisions(balls)

        window.fill(COLORS['black'])
        pygame.draw.circle(
            window,
            COLORS['white'],
            (int(CIRCLE_CENTER.x), int(CIRCLE_CENTER.y)),
            CIRCLE_RADIUS,
            3
        )
        for ball in balls:
            ball.draw(window)

        pygame.display.flip()

    pygame.quit()


if __name__ == '__main__':
    main()
