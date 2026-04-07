import random
import pygame

class RainParticle:
    def __init__(self, width, height):
        self.x = random.randint(0, width)
        self.y = random.randint(-height, 0)
        self.speed = random.randint(3000, 5000)
        self.length = random.randint(8, 15)

    def update(self, dt, width, height):
        self.y += self.speed * dt / 1000

        if self.y > height:
            self.x = random.randint(0, width)
            self.y = random.randint(-50, 0)

    def draw(self, surface):
        pygame.draw.line(
            surface,
            (180, 180, 200),
            (self.x, self.y),
            (self.x, self.y + self.length),
            1
        )


class RainSystem:
    def __init__(self, width, height, intensity=200):
        self.width = width
        self.height = height
        self.particles = [RainParticle(width, height) for _ in range(intensity)]

    def update(self, dt):
        for p in self.particles:
            p.update(dt, self.width, self.height)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)
