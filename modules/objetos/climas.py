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


class SunnyOverlay:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def draw(self, surface):
        # vinheta dourada suave nas bordas
        vignette = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        # desenha bordas com alpha crescente
        for i in range(250):  # número de camadas
            alpha = 120 - int(120 * (i / 250))  # alpha máximo ~50
            pygame.draw.rect(
                vignette,
                (255, 200, 100, alpha),  # dourado ensolarado
                (i, i, self.width - 2*i, self.height - 2*i),
                1
            )

        # aplica vinheta somando cor
        surface.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)


class CloudyOverlay:
    def __init__(self, width, height, cloud_count=15):
        self.width = width
        self.height = height
        # cada nuvem: x, y, tamanho, velocidade
        self.clouds = [
            [random.randint(0, width), random.randint(0, height),
             random.randint(80, 150), random.uniform(0.02, 0.1)]
            for _ in range(cloud_count)
        ]

    def update(self, dt):
        for c in self.clouds:
            c[0] += c[3] * dt  # movimento horizontal lento
            if c[0] > self.width + c[2]:
                c[0] = -c[2]
                c[1] = random.randint(0, self.height)

    def draw(self, surface):
        # vinheta cinza suave nas bordas
        vignette = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        for i in range(250):
            alpha = int(100 - (i * 0.4))
            pygame.draw.rect(
                vignette,
                (70, 70, 70, alpha),  # cinza neutro
                (i, i, self.width - 2*i, self.height - 2*i),
                1
            )
        surface.blit(vignette, (0, 0), special_flags=pygame.BLEND_RGBA_ADD)

        # camada translúcida geral (reduz saturação)
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((100, 100, 100, 200))
        surface.blit(overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

        # desenhar nuvens translúcidas
        for x, y, r, _ in self.clouds:
            cloud = pygame.Surface((r*2, r), pygame.SRCALPHA)
            pygame.draw.ellipse(cloud, (60, 60, 60, 3), (0, 0, r*2, r))
            surface.blit(cloud, (x-r, y-r//2), special_flags=pygame.BLEND_RGBA_ADD)