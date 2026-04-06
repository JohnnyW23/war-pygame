import pygame
import sys
import os


class Game:
    def __init__(self):
        from modules.exercito import Exercito

        pygame.init()

        # Configurações da janela
        self.width = 1600
        self.height = 800

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Simulador de Guerra")
        self.map_background = pygame.image.load("assets/map_model.jpg").convert()
        self.map_position = (640, 20, 940, 500)

        self.local_icons = {}

        locals = os.listdir('assets/local_icons')
        for local in locals:
            self.local_icons[local[:-4]] = pygame.image.load(f"assets/local_icons/{local}").convert_alpha()

        self.status_icons = {}

        statuses = os.listdir('assets/cards')
        for status in statuses:
            tamanho = (24, 24)
            imagem = pygame.image.load(f"assets/cards/{status}").convert_alpha()
            self.status_icons[status[:-4]] = pygame.transform.smoothscale(imagem, tamanho)

        # Cores
        self.cores = {
            "bg": (20, 25, 20),
            "secundaria": (5, 10, 5),
            "branco": (250, 250, 250),
            "darkgreen": (0, 45, 0),
            "amarelo": (248,214,0)
        }

        self.spritesheet = {
            "explosao": {
                "arquivo": pygame.image.load("assets/spritesheets/explosao.png").convert_alpha(),
                "layer": 0,
                "frame_index": 0
            }
        }

        self.sprite_explosao()

        # Fonte principal
        self.fonts = []
        for size in range(30):
            self.fonts.append(pygame.font.Font('fonts/JetBrainsMono-Regular.ttf', size=size))
        
        self.font_big = pygame.font.Font('fonts/DejaVuSans.ttf', size=55)

        self.renders = {
            "locais_dominados_texto": self.fonts[12].render("Locais dominados:", True, self.cores["branco"]),
            "status_dia_texto": self.fonts[28].render("Dia ", True, self.cores["branco"])
        }

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
        
        self.army_overlays = {}

        for exercito in self.exercitos:
            overlay = pygame.Surface((20, 20), pygame.SRCALPHA)
            overlay.fill((*exercito.cor, 170))
            self.army_overlays[exercito.id] = overlay

        self.exercito_index = 0

        self.tiles = []

        self.dia = 1
        self.hora = 0
        self.minutos = 0
        self.segundos = 0

        self.tempo_acumulado = 0

        self.logs = [
            self.fonts[10].render(f'=============== Dia {self.dia} ===============', True, self.cores["amarelo"]),
            self.fonts[10].render('', True, self.cores["amarelo"])
        ]

        self.line_height = 15
        self.scroll_offset = 0

        self.UPDATE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.UPDATE_EVENT, 1000)

        self.map_surface = pygame.Surface((940, 500), pygame.SRCALPHA)

        self.generate_map_tiles()
        self.territorios_iniciais()

        self.atualizar_horario()

        self.atualizar_status_weather()

        self.atualizar_army_cards()

        # Controle de FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.event_chance = 10

        # Controle do loop
        self.running = True
    

    def atualizar_horario(self):

        hora = int(self.hora)
        minutos = int(self.minutos)
        segundos = int(self.segundos)

        self.horario = f"[{hora:02}:{minutos:02}:{segundos:02}]"
        self.horario_formatado = f"[{hora:02}:{minutos:02}]"


    def run(self):
        while self.running:

            dt = self.clock.tick(self.FPS)
            self.tempo_acumulado += dt

            self.atualizar_tempo_jogo(dt)

            self.draw()
            self.events()

        pygame.quit()
        sys.exit()

    def atualizar_tempo_jogo(self, dt):

        # segundos visuais do relógio
        self.segundos += dt * 1.2

        if self.segundos >= 60:
            self.segundos -= 60
            self.minutos += 1

        if self.minutos >= 60:
            self.minutos -= 60
            self.hora += 1

        if self.hora >= 24:
            self.hora = 0
            self.dia += 1
            self.log('')
            self.log(f'=============== Dia {self.dia} ===============')
            self.log('')

        self.atualizar_status_weather()


    def events(self):
        from random import choice, randint

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEWHEEL:
                padding = 10
                line_height = 15

                visible_height = self.logs_screen.height - padding * 2
                total_height = len(self.logs) * line_height

                max_scroll = max(0, total_height - visible_height)

                self.scroll_offset -= event.y * 20

                if self.scroll_offset < 0:
                    self.scroll_offset = 0
                elif self.scroll_offset > max_scroll:
                    self.scroll_offset = max_scroll
     
            if event.type == self.UPDATE_EVENT:

                # sistema de chance
                if randint(1, 100) <= self.event_chance:

                    index = self.exercito_index
                    exercito = self.exercitos_ativos[index]
                    inimigo = choice(exercito.inimigos)

                    exercito.inimigo = inimigo

                    dado1 = randint(1, 100)
                    dado2 = randint(1, 100)

                    relogio = f"{self.horario}"

                    if dado1 > dado2:
                        self.expandir_territorio(exercito, dominate=True)
                        self.log(f"{relogio} {exercito.nome} atacou fortemente {inimigo.nome}!")

                    elif dado2 > dado1:
                        self.log(f"{relogio} {exercito.nome} tentou atacar {inimigo.nome}, mas foi repelido.")
                    else:
                        self.log(f"{relogio} {exercito.nome} e {inimigo.nome} lutaram, e houve um impasse.")

                    # reset da chance
                    self.event_chance = 10

                    # próximo exército
                    if index == len(self.exercitos_ativos) - 1:
                        self.exercito_index = 0
                    else:
                        self.exercito_index += 1

                else:
                    # aumenta chance se não ocorreu evento
                    self.event_chance = min(self.event_chance + 10, 100)


    def log(self, texto):
        padding = 10
        line_height = 15

        visible_height = self.logs_screen.height - padding * 2
        total_height = len(self.logs) * line_height

        max_scroll = max(0, total_height - visible_height)

        estava_no_fim = self.scroll_offset >= max_scroll - 5

        render = self.fonts[10].render(texto, True, self.cores["amarelo"])
        self.logs.append(render)

        self.logs = self.logs[-100:]

        total_height = len(self.logs) * line_height
        max_scroll = max(0, total_height - visible_height)

        if estava_no_fim:
            self.scroll_offset = max_scroll


    def generate_map_tiles(self):
        from modules.tile import Tile

        MAP_W = 47
        MAP_H = 25
        TILE = 20

        self.tiles = []

        for y in range(MAP_H):

            linha = []

            for x in range(MAP_W):

                rect = pygame.Rect(
                    640 + x * TILE,
                    20 + y * TILE,
                    TILE,
                    TILE
                )

                tile = Tile(None, (0,0,0), x, y, rect)

                linha.append(tile)

            self.tiles.append(linha)


    def draw(self):
        """Desenha na tela"""

        self.screen.fill(self.cores["bg"])
        self.atualizar_horario()
        self.draw_day_weather_status()
        self.draw_army_cards()
        self.draw_map_screen()
        self.draw_log_screen()
        pygame.draw.rect(self.screen, self.cores["darkgreen"], self.map_position, 3)
        self.processar_explosoes_agendadas()
        self.update_explosoes()
        fps = int(self.clock.get_fps())
        fps_text = self.fonts[12].render(f"FPS: {fps}", True, (255,255,255))
        self.screen.blit(fps_text, (10,10))

        pygame.display.flip()
    
    #SPRITES DE EXPLOSAO#

    def sprite_explosao(self):
        arquivo = self.spritesheet['explosao']['arquivo']
        layer = self.spritesheet['explosao']['layer']
        self.spritesheet['explosao']['frames'] = [self.get_frame(arquivo, i, 64, 64, layer) for i in range(12)]
        self.explosoes = []
        self.explosoes_agendadas = []

    def update_explosoes(self):
        for explosao in self.explosoes:
            explosao.update()
            explosao.draw(self.screen)

        self.explosoes = [e for e in self.explosoes if not e.finished]
        self.explosoes = self.explosoes[-30:]

    def agendar_explosoes(self, x, y):
        from random import randint

        if len(self.explosoes_agendadas) > 15:
            return

        agora = pygame.time.get_ticks()

        for i in range(randint(3, 5)):
            delay = randint(200, 400) * i
            self.explosoes_agendadas.append({
                "tempo": agora + delay,
                "x": randint(x - 32, x - 12),
                "y": randint(y - 32, y - 12)
            })
    
    def processar_explosoes_agendadas(self):
        from modules.explosao import Explosao

        agora = pygame.time.get_ticks()

        for explosao in self.explosoes_agendadas[:]:

            if len(self.explosoes) >= 20:
                break

            if agora >= explosao["tempo"]:
                self.explosoes.append(
                    Explosao(
                        explosao["x"],
                        explosao["y"],
                        self.spritesheet["explosao"]["frames"]
                    )
                )
                self.explosoes_agendadas.remove(explosao)


    def draw_day_weather_status(self):
        self.screen_day_weather_status = pygame.Rect(20, 20, 600, 60)
        pygame.draw.rect(self.screen, self.cores["secundaria"], self.screen_day_weather_status)
        pygame.draw.rect(self.screen, self.cores["darkgreen"], self.screen_day_weather_status, 3)

        self.screen.blit(self.renders["status_dia_texto"], (40, 30))

        cache = self.status_weather_cache

        self.screen.blit(cache["dia"], (100, 30))
        self.screen.blit(cache["horario"], (160, 30))




    def draw_army_cards(self):
        x_minimo = 20
        y_minimo = self.screen_day_weather_status.height + 40

        self.army_cards = {}

        for index, exercito in enumerate(self.exercitos):
            if index == 0: card = pygame.Rect(x_minimo, y_minimo, 290, 330)
            elif index == 1: card = pygame.Rect(x_minimo + 310, y_minimo, 290, 330)
            elif index == 2: card = pygame.Rect(x_minimo, y_minimo + 350, 290, 330)
            elif index == 3: card = pygame.Rect(x_minimo + 310, y_minimo + 350, 290, 330)

            pygame.draw.rect(self.screen, self.cores["secundaria"], card)
            pygame.draw.rect(self.screen, self.cores["darkgreen"], card, 3)

             # --- Textos dentro do card ---
            cache = self.army_card_cache[exercito.id]

            self.screen.blit(cache["nome"], (card.x + 10, card.y + 10))
            self.screen.blit(cache["marechal"], (card.x + 10, card.y + 40))
            self.screen.blit(cache["perfil"], (card.x + 10, card.y + 60))
            self.screen.blit(cache["territorios"], (card.x + 10, card.y + 80))
            self.screen.blit(cache["poder"], (card.x + card.width - 45, card.y + 5))

            for index, value in enumerate(self.status_icons.values()):
                if index == 0:
                    self.screen.blit(value, (card.x + 35, card.y + 120))
                else:
                    self.screen.blit(value, (card.x + 35 + (50 * index), card.y + 120))
            
            for index, atributo in enumerate(cache["atributos"]):
                if index == 0:
                    self.screen.blit(atributo, (card.x + 36, card.y + 154))
                else:
                    self.screen.blit(atributo, (card.x + 36 + (50 * index), card.y + 154))
            
            self.screen.blit(self.renders["locais_dominados_texto"], (card.x + 10, card.y + 185))
            
            local_y = 205

            for local in cache["locais"]:

                self.screen.blit(local, (card.x + 10, card.y + local_y))

                local_y += 15
    

    def atualizar_status_weather(self):
        cache = {}

        cache["dia"] = self.fonts[28].render(f"{self.dia}", True, self.cores["amarelo"])

        cache["horario"] = self.fonts[28].render(self.horario_formatado, True, self.cores["amarelo"])

        self.status_weather_cache = cache
    

    def atualizar_army_cards(self):

        from modules.num_romano import numeros_romanos

        self.army_card_cache = {}

        for exercito in self.exercitos:

            cache = {}

            cache["nome"] = self.fonts[16].render(exercito.nome, True, exercito.cor)

            cache["marechal"] = self.fonts[12].render(
                f"Marechal {exercito.marechal.nome}",
                True,
                (200,200,200)
            )

            cache["perfil"] = self.fonts[12].render(
                exercito.marechal.perfil,
                True,
                exercito.marechal.cor
            )

            cache["poder"] = self.font_big.render(
                numeros_romanos[exercito.poder][0],
                True,
                exercito.cor
            )

            cache["territorios"] = self.fonts[12].render(
                f"Territórios: {len(exercito.tiles)}",
                True,
                self.cores["branco"]
            )

            cache["atributos"] = []

            for atributo in [
                exercito.forca,
                exercito.tecnologia,
                exercito.suprimentos,
                exercito.moral,
                exercito.estrategia
            ]:

                cache["atributos"].append(
                    self.fonts[12].render(str(atributo), True, self.cores["branco"])
                )

            cache["locais"] = []

            for local in exercito.locais:
                if local[1] == "comum":
                    cor = (0, 200, 0)
                elif local[1] == "incomum":
                    cor = (0, 200, 200)
                else:
                    cor = (200, 200, 0)

                cache["locais"].append(
                    self.fonts[10].render(f"> {local[0]}", True, cor)
                )

            self.army_card_cache[exercito.id] = cache
                
    
    def draw_map_screen(self):

        self.screen.blit(self.map_background, (640, 20))
        self.screen.blit(self.map_surface, (640, 20))
    

    def draw_log_screen(self):
        x_minimo = self.screen_day_weather_status.width + 40
        y_minimo = 540

        self.logs_screen = pygame.Rect(x_minimo, y_minimo, 1580 - x_minimo, 240)

        pygame.draw.rect(self.screen, self.cores["secundaria"], self.logs_screen)
        pygame.draw.rect(self.screen, self.cores["darkgreen"], self.logs_screen, 3)

        # ativa corte (clip)
        logs_clip = pygame.Rect(x_minimo, y_minimo + 10, 1580 - x_minimo, 220)
        self.screen.set_clip(logs_clip)

        padding = 10
        line_height = 15

        y = self.logs_screen.y + padding - self.scroll_offset

        for log in self.logs:
            self.screen.blit(log, (self.logs_screen.x + padding, y))
            y += line_height

        self.screen.set_clip(None)

    def territorios_iniciais(self):
        from modules.local import gerar_local
        from random import choice, randint

        # escolher um tile inicial aleatório para cada exército
        for exercito in self.exercitos:
            # pega todos os tiles disponíveis (sem dono)
            todos_tiles = []
            for linha in self.tiles:
                for tile in linha:
                    if tile.dono is None:
                        todos_tiles.append(tile)

            # escolhe um tile aleatório
            tile_inicial = choice(todos_tiles)

            # marca como território inicial
            tile_inicial.dono = exercito
            exercito.tiles.append(tile_inicial)

        # expansão dos territórios
        for _ in range(179):
            for exercito in self.exercitos:
                self.expandir_territorio(exercito)
            
        for exercito in self.exercitos:
            locais = randint(5, 7)

            for _ in range(locais):
                tile = choice(exercito.tiles)
                tile.local = gerar_local()
                exercito.locais.append([tile.local.nome, tile.local.raridade])
                self.atualizar_tile_visual(tile)


    def expandir_territorio(self, exercito, dominate=False):
        from random import choice

        tiles_disponiveis = set()
        for tile in exercito.tiles:
            # coordenadas do tile atual
            x = tile.x
            y = tile.y

            # possíveis vizinhos
            vizinhos = [
                (x + 1, y),
                (x - 1, y),
                (x, y + 1),
                (x, y - 1)
            ]

            for vx, vy in vizinhos:

                if 0 <= vx < 47 and 0 <= vy < 25:

                    vizinho = self.tiles[vy][vx]
                    if not dominate:
                        if vizinho.dono is None:
                            tiles_disponiveis.add(vizinho)
                    else:
                        if vizinho.dono is None or vizinho.dono is exercito.inimigo:
                            tiles_disponiveis.add(vizinho)

        # se houver tiles disponíveis, conquista um aleatório
        if tiles_disponiveis:
            novo_tile = choice(list(tiles_disponiveis))
            antigo_dono = novo_tile.dono
            if antigo_dono is not None:
                antigo_dono.tiles.remove(novo_tile)
                self.agendar_explosoes(novo_tile.tile.x, novo_tile.tile.y)
                if novo_tile.local is not None:
                    antigo_dono.locais.remove([novo_tile.local.nome, novo_tile.local.raridade])
                    exercito.locais.append([novo_tile.local.nome, novo_tile.local.raridade])
            novo_tile.dono = exercito
            exercito.tiles.append(novo_tile)
            self.atualizar_tile_visual(novo_tile)
            self.atualizar_army_cards()


    def atualizar_tile_visual(self, tile):
        x = tile.tile.x - self.map_position[0]
        y = tile.tile.y - self.map_position[1]

        # limpa o tile
        pygame.draw.rect(self.map_surface, (0,0,0,0), (x, y, 20, 20))

        overlay = self.army_overlays[tile.dono.id]
        self.map_surface.blit(overlay, (x, y))

        if tile.local and tile.local.tipo in self.local_icons:
            imagem = self.local_icons[tile.local.tipo]
            self.map_surface.blit(imagem, (x + 2, y + 2))
    

    def get_frame(self, sheet, frame, width, height, layer):
        rect = pygame.Rect(frame * width, layer * height, width, height)
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), rect)
        return image


if __name__ == "__main__":

    game = Game()
    game.run()
