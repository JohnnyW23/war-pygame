class Explosao:
    def __init__(self, x, y, frames):
        self.x = x
        self.y = y
        self.frames = frames
        self.frame = 0
        self.timer = 0
        self.speed = 4  # velocidade da animação
        self.finished = False

    def update(self):
        self.timer += 1

        if self.timer >= self.speed:
            self.timer = 0
            self.frame += 1

            if self.frame >= len(self.frames):
                self.finished = True

    def draw(self, screen):
        if not self.finished:
            screen.blit(self.frames[self.frame], (self.x, self.y))