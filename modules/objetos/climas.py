import random
import pygame

class RainParticle:
    def __init__(self, width, height, angle):
        self.width = width
        self.height = height
        self.angle = angle
        self.reset()

    def reset(self):
        # spawn em uma faixa que cobre topo e esquerda
        self.x = random.randint(-self.height, self.width)
        self.y = random.randint(-self.height, 0)
        self.speed = random.randint(700, 1000)
        self.length = random.randint(9, 16)

    def update(self, dt):
        self.y += self.speed * dt / 1000
        self.x += self.angle * self.speed * dt / 1000 / 2

        if self.y > self.height or self.x > self.width:
            self.reset()

    def draw(self, surface):
        pygame.draw.line(
            surface,
            (50, 50, 130),
            (self.x, self.y),
            (self.x + self.angle * self.length, self.y + self.length),
            1
        )


class RainSystem:
    def __init__(self, width, height, intensity, angle=0.3):
        self.width = width
        self.height = height
        self.particles = [RainParticle(width, height, angle) for _ in range(intensity)]

    def update(self, dt):
        for p in self.particles:
            p.update(dt)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class TemperatureOverlay:
    def __init__(self, width, height, color):
        self.width = width
        self.height = height
        self.color = color

    def draw(self, surface):
        # vinheta dourada suave nas bordas
        vignette = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # desenha bordas com alpha crescente
        for i in range(125):
            alpha = int(130 - (i * 1.04))
            pygame.draw.rect(
                vignette,
                (*self.color, alpha),
                (i, i, self.width - 2*i, self.height - 2*i),
                1
            )

        # aplica vinheta somando cor
        surface.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)



class LightningBlink:
    def __init__(self, map_rect, cooldown_range=(1000, 5000)):
        self.map_rect = map_rect
        self.timer = 0
        self.cooldown_range = cooldown_range
        self.cooldown = random.randint(*self.cooldown_range)
        self.active = False

    def update(self, dt):
        self.timer += dt

        if not self.active and self.timer >= self.cooldown:
            self.active = True
            self.timer = 0
            self.blinks = 2

        elif self.active:
            self.blinks -= 1
            if self.blinks <= 0:
                self.active = False
                self.timer = 0
                self.cooldown = random.randint(*self.cooldown_range)

    def draw(self, screen):
        if not self.active:
            return

        # pisca SOMENTE na área do mapa
        screen.fill(
            (255, 255, 255),
            self.map_rect,
            special_flags=pygame.BLEND_RGB_ADD
        )


class FogMoving:
    def __init__(self, width, height, speed=20, alpha=30):
        self.width = width
        self.height = height
        self.speed = speed
        self.fog_surface = pygame.Surface((width, height), pygame.SRCALPHA)

        for _ in range(120):
            value = random.randint(100, 150)
            x = random.randint(0, width)
            y = random.randint(0, height)
            r = random.randint(80, 160)
            pygame.draw.circle(
                self.fog_surface,
                (value, value, value, alpha),
                (x, y),
                r
            )

        self.offset = 0

    def update(self, dt):
        self.offset += self.speed * dt / 1000
        if self.offset >= self.width:
            self.offset = 0

    def draw(self, surface):
        x = int(self.offset)

        surface.blit(self.fog_surface, (-x, 0), special_flags=pygame.BLEND_RGBA_ADD)
        surface.blit(self.fog_surface, (-x + self.width, 0), special_flags=pygame.BLEND_RGBA_ADD)


class CloudyOverlay:
    def __init__(self, width, height):
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((50, 50, 70, 100))  # azul-acinzentado escuro

    def draw(self, surface):
        surface.blit(self.overlay, (0, 0))


class WindParticle:
    def __init__(self, width, height, direction=1):
        self.width = width
        self.height = height
        self.direction = direction
        self.reset()

    def reset(self):
        self.x = random.randint(0, self.width)
        self.y = random.randint(0, self.height)
        self.speed = random.randint(300, 700)
        self.length = random.randint(15, 40)

    def update(self, dt):
        self.x += self.speed * dt / 1000 * self.direction

        if self.x > self.width or self.x < -self.length:
            self.reset()
            self.x = -self.length if self.direction > 0 else self.width

    def draw(self, surface):
        alpha = random.randint(80, 180)
        pygame.draw.line(
            surface,
            (200, 200, 200, alpha),
            (self.x, self.y),
            (self.x - self.length * self.direction, self.y),
            1
        )

class WindSystem:
    def __init__(self, width, height, intensity=120, direction=1):
        self.particles = [
            WindParticle(width, height, direction)
            for _ in range(intensity)
        ]

    def update(self, dt):
        for p in self.particles:
            p.update(dt)

    def draw(self, surface):
        for p in self.particles:
            p.draw(surface)


class WindOverlay:
    def __init__(self, width, height):
        self.overlay = pygame.Surface((width, height), pygame.SRCALPHA)
        self.overlay.fill((200, 200, 210, 40))

    def draw(self, surface):
        surface.blit(self.overlay, (0, 0))
