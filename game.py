import pygame
import sys


class Game:
    def __init__(self):
        from modules.exercito import Exercito

        pygame.init()

        # Configurações da janela
        self.width = 1600
        self.height = 800
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulador de Guerra")

        # Controle de FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        # Controle do loop
        self.running = True

        # Cores
        self.cores = {
            "bg": (20, 25, 20),
            "secundaria": (5, 10, 5),
            "branco": (250, 250, 250)
        }

        # Fonte principal
        self.fonts = []
        for size in range(21):
            self.fonts.append(pygame.font.Font('war pygame/fonts/JetBrainsMono-Regular.ttf', size=size))


        self.exercitos = [
            Exercito(0, "Saint Louis", (255, 20, 20), "Resistência Popular", "RSP"),
            Exercito(1, "Viena Empire", (0, 190, 255), "Voz Patriótica", "VPT"),
            Exercito(2, "República Ashbury", (0, 255, 0), "Som da Liberdade", "SDL"),
            Exercito(3, "Alta Galileia", (220, 150, 220), "Sanctum Dominium", "SDM")
        ]

        self.exercitos_ativos = self.exercitos[:]

        for exercito in self.exercitos:
            for inimigo in self.exercitos:
                if exercito != inimigo:
                    exercito.inimigos.append(inimigo)

        self.exercito_index = 0

        self.tiles = {}

        self.UPDATE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.UPDATE_EVENT, 1000)

        self.draw_start()

    def run(self):
        while self.running:
            self.events()
            self.update()
            self.draw()

            self.clock.tick(self.FPS)

        pygame.quit()
        sys.exit()

    def events(self):
        from random import choice

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == self.UPDATE_EVENT:
                index = self.exercito_index
                exercito = self.exercitos_ativos[index]
                inimigo = choice(exercito.inimigos)

                self.expandir_territorio(exercito)
                
                if index == len(self.exercitos_ativos) - 1:
                    self.exercito_index = 0
                else:
                    self.exercito_index += 1

    def update(self):
        """Atualiza a lógica do jogo"""
        pass

    def draw(self):
        """Desenha na tela"""

        pygame.display.flip()
    
    def draw_start(self):
        self.screen.fill(self.cores["bg"])
        self.draw_day_weather_status()
        self.draw_army_cards()
        self.draw_map_screen()
        self.territorios_iniciais()

    def draw_day_weather_status(self):
        self.screen_day_weather_status = pygame.Rect(20, 20, 600, 60)
        pygame.draw.rect(self.screen, self.cores["secundaria"], self.screen_day_weather_status)

        # LINHA TESTE
        pygame.draw.rect(self.screen, (255, 0, 0), (self.width // 2, 0, 2, self.height))


    def draw_army_cards(self):
        from modules.num_romano import numeros_romanos

        x_minimo = 20
        y_minimo = self.screen_day_weather_status.height + 40

        self.army_cards = {}

        for index, exercito in enumerate(self.exercitos):
            if index == 0: card = pygame.Rect(x_minimo, y_minimo, 290, 330)
            elif index == 1: card = pygame.Rect(x_minimo + 310, y_minimo, 290, 330)
            elif index == 2: card = pygame.Rect(x_minimo, y_minimo + 350, 290, 330)
            elif index == 3: card = pygame.Rect(x_minimo + 310, y_minimo + 350, 290, 330)

            pygame.draw.rect(self.screen, self.cores["secundaria"], card)

             # --- Textos dentro do card ---
            # Nome do exército
            nome_text = self.fonts[16].render(exercito.nome, True, exercito.cor)
            self.screen.blit(nome_text, (card.x + 10, card.y + 10))

            # Nome do marechal
            marechal_text = self.fonts[12].render(f"Marechal {exercito.marechal.nome}", True, (200, 200, 200))
            self.screen.blit(marechal_text, (card.x + 10, card.y + 40))

            # Perfil do marechal (com cor específica)
            perfil_text = self.fonts[12].render(exercito.marechal.perfil, True, exercito.marechal.cor)
            self.screen.blit(perfil_text, (card.x + 10, card.y + 60))

            # Nível de poder do exército
            fonte = pygame.font.Font('war pygame/fonts/DejaVuSans.ttf', size=55)
            poder_text = fonte.render(numeros_romanos[exercito.poder][0], True, exercito.cor)
            self.screen.blit(poder_text, (card.x + card.width - numeros_romanos[exercito.poder][1], card.y + 5))

            self.army_cards[exercito.id] = {
                "card": card,
                "texto_nome": nome_text,
                "texto_marechal": marechal_text,
                "texto_perfil": perfil_text
            }
    
    def draw_map_screen(self):
        from modules.tile import Tile
        x_minimo = self.screen_day_weather_status.width + 40
        y_minimo = 20

        background = pygame.image.load("war pygame/assets/map_model.jpg")
        self.screen.blit(background, (x_minimo, y_minimo))

        # self.map = pygame.Rect(x_minimo, y_minimo, 1580 - x_minimo, 500)
        # pygame.draw.rect(self.screen, (0, 0, 0), self.map)

        # 940 x 500

        for y in range(0, 25):
            y_value = y * 20
            self.tiles[y_value] = {}
            for x in range(0, 47):
                x_value = x * 20

                tile = pygame.Rect(x_minimo + x_value, y_minimo + y_value, 20, 20)
                self.tiles[y_value][x_value] = Tile(None, (0, 0, 0), x_value, y_value, tile)


    def territorios_iniciais(self):
        from random import choice
        # escolher um tile inicial aleatório para cada exército
        for exercito in self.exercitos:
            # pega todos os tiles disponíveis (sem dono)
            todos_tiles = []
            for y_dict in self.tiles.values():
                for tile in y_dict.values():
                    if tile.dono is None:
                        todos_tiles.append(tile)

            # escolhe um tile aleatório
            tile_inicial = choice(todos_tiles)

            # marca como território inicial
            tile_inicial.dono = exercito
            exercito.tiles.append(tile_inicial)
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            s.fill((*exercito.cor, 170))
            self.screen.blit(s, tile_inicial.tile.topleft)
            # pygame.draw.rect(self.screen, exercito.cor, tile_inicial.tile)

        # expansão dos territórios
        for round in range(180):
            for exercito in self.exercitos:
                self.expandir_territorio(exercito)

    

    def expandir_territorio(self, exercito):
        from random import choice

        tiles_disponiveis = []
        for tile in exercito.tiles:
            # coordenadas do tile atual
            x = tile.x
            y = tile.y

            # possíveis vizinhos
            vizinhos = [
                (x + 20, y),     # direita
                (x - 20, y),     # esquerda
                (x, y + 20),     # abaixo
                (x, y - 20)      # acima
            ]

            for vx, vy in vizinhos:
                if vy in self.tiles and vx in self.tiles[vy]:
                    vizinho = self.tiles[vy][vx]
                    if vizinho.dono is None:
                        tiles_disponiveis.append(vizinho)

        # se houver tiles disponíveis, conquista um aleatório
        if tiles_disponiveis:
            novo_tile = choice(tiles_disponiveis)
            novo_tile.dono = exercito
            exercito.tiles.append(novo_tile)
            s = pygame.Surface((20, 20), pygame.SRCALPHA)
            s.fill((*exercito.cor, 170))
            self.screen.blit(s, novo_tile.tile.topleft)
            # pygame.draw.rect(self.screen, exercito.cor, novo_tile.tile)

            
if __name__ == "__main__":

    game = Game()
    game.run()