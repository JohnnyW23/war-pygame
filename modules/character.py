import os
from random import choice, randint
import pygame


class Character:
    def __init__(self, head, body, hair, eyes, eyebrowns, facial_hair, torso, suspenders, legs, feet):
        self.parts = [body, head, hair, eyes, eyebrowns, facial_hair, torso, suspenders, legs, feet]

        self.frame_width = self.parts[0].get_width() // self.get_num_columns(self.parts[0])
        self.frame_height = self.parts[0].get_height() // 4  # 4 fileiras

        self.current_frame = 0
        self.animation_timer = 0
        self.animation_speed = 800  # ms por frame

        # 0 = trás, 1 = esquerda, 2 = frente, 3 = direita
        self.direction_row = 3  # começa olhando pra direita

        # timer para mudar direção
        self.direction_timer = 0
        self.direction_change_interval = randint(2000, 7000)  # a cada 3 segundos pode mudar

    def get_num_columns(self, sprite):
        return sprite.get_width() // (sprite.get_height() // 4)

    def get_frame(self, frame_index):
        rect = pygame.Rect(frame_index * self.frame_width,
                           self.direction_row * self.frame_height,
                           self.frame_width, self.frame_height)
        composed = pygame.Surface((self.frame_width, self.frame_height), pygame.SRCALPHA)

        for part in self.parts:
            if part is not None:
                frame = part.subsurface(rect)
                composed.blit(frame, (0, 0))

        return composed

    def update(self, dt):
        # animação
        self.animation_timer += dt
        if self.animation_timer >= self.animation_speed:
            self.animation_timer = 0
            self.current_frame = (self.current_frame + 1) % self.get_num_columns(self.parts[0])

        # mudança aleatória de direção
        self.direction_timer += dt
        if self.direction_timer >= self.direction_change_interval:
            self.direction_timer = 0
            self.direction_change_interval = randint(2000, 7000)  # nova duração para próxima mudança
            # sorteia entre esquerda (1), frente (2) e direita (3)
            self.direction_row = choice([1, 2, 3])

    def draw(self, surface, pos):
        frame = self.get_frame(self.current_frame)
        surface.blit(frame, pos)


def generate_head(skin_color):
    return pygame.image.load(f'assets/characters/heads/{skin_color}/Idle.png').convert_alpha()


def generate_body(skin_color):
    return pygame.image.load(f'assets/characters/body/{skin_color}/Idle.png').convert_alpha()


def generate_hair():
    hair_styles = [f for f in os.listdir('assets/characters/hairs') if os.path.isdir(os.path.join('assets/characters/hairs', f))]
    hair_style = choice(hair_styles)
    hair_colors = [f for f in os.listdir(f'assets/characters/hairs/{hair_style}') if os.path.isdir(os.path.join('assets/characters/hairs', hair_style, f))]
    hair_color = choice(hair_colors)
    return pygame.image.load(f'assets/characters/hairs/{hair_style}/{hair_color}/Idle.png').convert_alpha()


def generate_eyes():
    eye_colors = [f for f in os.listdir('assets/characters/eyes') if os.path.isdir(os.path.join('assets/characters/eyes', f))]
    eye_color = choice(eye_colors)
    return pygame.image.load(f'assets/characters/eyes/{eye_color}/Idle.png').convert_alpha()


def generate_eyebrowns():
    eyebrown_types = [f for f in os.listdir('assets/characters/eyebrowns') if os.path.isdir(os.path.join('assets/characters/eyebrowns', f))]
    eyebrown_type = choice(eyebrown_types)
    eyebrowns_colors = [f for f in os.listdir(f'assets/characters/eyebrowns/{eyebrown_type}') if os.path.isdir(os.path.join('assets/characters/eyebrowns', eyebrown_type, f))]
    eyebrowns_color = choice(eyebrowns_colors)
    return pygame.image.load(f'assets/characters/eyebrowns/{eyebrown_type}/{eyebrowns_color}/Idle.png').convert_alpha()


def generate_facial_hair():
    from random import randint
    if randint(1, 3) == 1:
        return None
    facial_hair_types = [f for f in os.listdir('assets/characters/facial_hair') if os.path.isdir(os.path.join('assets/characters/facial_hair', f))]
    facial_hair_type = choice(facial_hair_types)
    facial_hair_colors = [f for f in os.listdir(f'assets/characters/facial_hair/{facial_hair_type}') if os.path.isdir(os.path.join('assets/characters/facial_hair', facial_hair_type, f))]
    facial_hair_color = choice(facial_hair_colors)
    return pygame.image.load(f'assets/characters/facial_hair/{facial_hair_type}/{facial_hair_color}/Idle.png').convert_alpha()


def generate_torso():
    torso_types = [f for f in os.listdir('assets/characters/torsos') if os.path.isdir(os.path.join('assets/characters/torsos', f))]
    torso_type = choice(torso_types)
    torso_colors = [f for f in os.listdir(f'assets/characters/torsos/{torso_type}') if os.path.isdir(os.path.join('assets/characters/torsos', torso_type, f))]
    torso_color = choice(torso_colors)
    return pygame.image.load(f'assets/characters/torsos/{torso_type}/{torso_color}/Idle.png').convert_alpha()


def generate_suspenders():
    from random import randint
    if randint(1, 5) < 5:
        return None
    suspender_colors = [f for f in os.listdir('assets/characters/suspender') if os.path.isdir(os.path.join('assets/characters/suspender', f))]
    suspender_color = choice(suspender_colors)
    return pygame.image.load(f'assets/characters/suspender/{suspender_color}/Idle.png').convert_alpha()


def generate_legs():
    leg_types = [f for f in os.listdir('assets/characters/legs') if os.path.isdir(os.path.join('assets/characters/legs', f))]
    leg_type = choice(leg_types)
    leg_colors = [f for f in os.listdir(f'assets/characters/legs/{leg_type}') if os.path.isdir(os.path.join('assets/characters/legs', leg_type, f))]
    leg_color = choice(leg_colors)
    return pygame.image.load(f'assets/characters/legs/{leg_type}/{leg_color}/Idle.png').convert_alpha()


def generate_feet():
    foot_types = [f for f in os.listdir('assets/characters/feet') if os.path.isdir(os.path.join('assets/characters/feet', f))]
    foot_type = choice(foot_types)
    foot_colors = [f for f in os.listdir(f'assets/characters/feet/{foot_type}') if os.path.isdir(os.path.join('assets/characters/feet', foot_type, f))]
    foot_color = choice(foot_colors)
    return pygame.image.load(f'assets/characters/feet/{foot_type}/{foot_color}/Idle.png').convert_alpha()


def generate_character():
    skin_color = choice(os.listdir('assets/characters/heads'))
    head = generate_head(skin_color)
    body = generate_body(skin_color)
    hair = generate_hair()
    eyes = generate_eyes()
    eyebrowns = generate_eyebrowns()
    facial_hair = generate_facial_hair()
    torso = generate_torso()
    suspenders = generate_suspenders()
    legs = generate_legs()
    feet = generate_feet()

    return Character(head, body, hair, eyes, eyebrowns, facial_hair, torso, suspenders, legs, feet)