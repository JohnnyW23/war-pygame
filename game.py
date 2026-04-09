import pygame
import sys
import os


class Game:
    def __init__(self):
        from modules.objetos.exercito import Exercito
        from modules.objetos.climas import RainSystem, TemperatureOverlay, CloudyOverlay, FogMoving, LightningBlink, WindOverlay, WindSystem

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
            "explosao1": {
                "arquivo": pygame.image.load("assets/spritesheets/explosao1.png").convert_alpha(),
                "layer": 0,
                "frame_index": 0
            },
            "explosao2": {
                "arquivo": pygame.image.load("assets/spritesheets/explosao2.png").convert_alpha(),
                "layer": 0,
                "frame_index": 0
            }
        }

        self.sprite_explosao()

        # Fonte principal
        self.fontsJB = []
        for size in range(30):
            self.fontsJB.append(pygame.font.Font('fonts/JetBrainsMono-Regular.ttf', size=size))
        
        self.fontDVS = pygame.font.Font('fonts/DejaVuSans.ttf', size=20)

        self.renders = {
            "locais_dominados_texto": self.fontsJB[12].render("Locais dominados:", True, self.cores["branco"]),
            "status_dia_texto": self.fontsJB[28].render("Dia ", True, self.cores["branco"])
        }

        self.climas = {
            "ensolarado": (pygame.image.load("assets/clima/ensolarado.png"), 0.31),
            "nublado": (pygame.image.load("assets/clima/nublado.png"), 0.15),
            "chuva leve": (pygame.image.load("assets/clima/chuva leve.png"), 0.10),
            "chuva forte": (pygame.image.load("assets/clima/chuva forte.png"), 0.07),
            "tempestade": (pygame.image.load("assets/clima/tempestade.png"), 0.05),
            "tormenta elétrica": (pygame.image.load("assets/clima/tormenta eletrica.png"), 0.02),
            "ventania": (pygame.image.load("assets/clima/ventania.png"), 0.05),
            "nevoeiro": (pygame.image.load("assets/clima/nevoeiro.png"), 0.05),
            "frio": (pygame.image.load("assets/clima/frio.png"), 0.15),
            "calor extremo": (pygame.image.load("assets/clima/calor extremo.png"), 0.05)
        }

        self.map_rect = pygame.Rect(640, 20, 940, 500)

        self.clima_surface = pygame.Surface(
            self.map_rect.size,
            pygame.SRCALPHA
        )

        self.chuva_leve = RainSystem(940, 500, intensity=150, angle=0.2)
        self.chuva_forte = RainSystem(940, 500, intensity=500, angle=0.5)
        self.cold_overlay = TemperatureOverlay(940, 500, (100, 200, 255))
        self.extreme_hot_overlay = TemperatureOverlay(940, 500, (255, 80, 60))
        self.cloudy_overlay = CloudyOverlay(940, 500)
        self.nevoeiro = FogMoving(940, 500)
        self.lightning = LightningBlink(self.map_rect)
        self.tormenta_eletrica = RainSystem(940, 500, intensity=900, angle=0.8)
        self.lightning_tormenta_eletrica = LightningBlink(self.map_rect, cooldown_range=(500, 1500))
        self.fog_wind = FogMoving(self.map_rect.width, self.map_rect.height, speed=30, alpha=20)
        self.wind_overlay = WindOverlay(940, 500)
        self.wind_system = WindSystem(940, 500, intensity=120, direction=1)


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

        self.clima = self.escolher_clima()

        self.dia = 1
        self.hora = 0
        self.minutos = 0
        self.segundos = 0

        self.tempo_acumulado = 0

        self.logs = [
            self.fontsJB[10].render(f'=============== Dia {self.dia} ===============', True, self.cores["amarelo"]),
            self.fontsJB[10].render('', True, self.cores["amarelo"])
        ]

        self.line_height = 15
        self.scroll_offset = 0

        self.locais_area = {}
        self.locais_scroll = {}

        self.UPDATE_EVENT = pygame.USEREVENT + 1
        pygame.time.set_timer(self.UPDATE_EVENT, 1000)

        self.map_surface = pygame.Surface((940, 500), pygame.SRCALPHA)

        self.generate_map_tiles()
        self.territorios_iniciais()

        self.atualizar_horario()

        self.atualizar_status_weather()

        # Controle de FPS
        self.clock = pygame.time.Clock()
        self.FPS = 60

        self.dt = self.clock.tick(self.FPS)

        self.event_chance = 5

        # Controle do loop
        self.running = True

        self.guerra_ativa = True

        self.atualizar_army_cards()
    

    def atualizar_horario(self):

        hora = int(self.hora)
        minutos = int(self.minutos)
        segundos = int(self.segundos)

        self.horario = f"[{hora:02}:{minutos:02}:{segundos:02}]"
        self.horario_formatado = f"[{hora:02}:{minutos:02}]"
    

    def draw_efeito_clima(self):
        self.clima_surface.fill((0, 0, 0, 0))

        dt = self.clock.tick(60)

        if self.clima[0] == 'Chuva leve':
            self.cloudy_overlay.draw(self.clima_surface)
            self.chuva_leve.update(dt)
            self.chuva_leve.draw(self.clima_surface)
        
        elif self.clima[0] == 'Chuva forte':
            self.cloudy_overlay.draw(self.clima_surface)
            self.chuva_forte.update(dt)
            self.chuva_forte.draw(self.clima_surface)
        
        elif self.clima[0] == 'Frio':
            self.cold_overlay.draw(self.clima_surface)
        
        elif self.clima[0] == 'Nevoeiro':   
            self.cloudy_overlay.draw(self.clima_surface)
            self.nevoeiro.update(dt)
            self.nevoeiro.draw(self.clima_surface)

        elif self.clima[0] == 'Calor extremo':
            self.extreme_hot_overlay.draw(self.clima_surface)
        
        elif self.clima[0] == 'Nublado':
            self.cloudy_overlay.draw(self.clima_surface)
        
        elif self.clima[0] == 'Tempestade':
            self.cloudy_overlay.draw(self.clima_surface)
            self.chuva_forte.update(dt)
            self.chuva_forte.draw(self.clima_surface)
        
        elif self.clima[0] == 'Tormenta elétrica':
            self.cloudy_overlay.draw(self.clima_surface)
            self.tormenta_eletrica.update(dt)
            self.tormenta_eletrica.draw(self.clima_surface)
        
        elif self.clima[0] == 'Ventania':
            self.wind_overlay.draw(self.clima_surface)
            self.wind_system.update(dt)
            self.wind_system.draw(self.clima_surface)
            self.fog_wind.update(dt)
            self.fog_wind.draw(self.clima_surface)

        self.screen.blit(self.clima_surface, self.map_rect.topleft)
        
        if self.clima[0] == 'Tempestade':
            self.lightning.update(dt)
            self.lightning.draw(self.screen)
        
        elif self.clima[0] == 'Tormenta elétrica':
            self.lightning_tormenta_eletrica.update(dt)
            self.lightning_tormenta_eletrica.draw(self.screen)


    def escolher_clima(self):
        from random import choices

        climas = self.climas

        nomes = list(climas.keys())
        probabilidades = [climas[c][1] for c in nomes]
        
        clima_escolhido = choices(nomes, weights=probabilidades, k=1)[0]
        imagem = climas[clima_escolhido][0]
        
        return [clima_escolhido.capitalize(), imagem]
    

    def run(self):
        while self.running:
            dt = self.clock.tick(self.FPS)
            self.tempo_acumulado += dt

            self.atualizar_tempo_jogo(dt)

            self.draw()
            if self.guerra_ativa:
                self.events()

        pygame.quit()
        sys.exit()


    def atualizar_tempo_jogo(self, dt):
        # segundos visuais do relógio
        self.segundos += dt * 3

        if self.segundos >= 60:
            self.segundos -= 60
            self.minutos += 1

        if self.minutos >= 60:
            self.minutos -= 60
            self.hora += 1

        if self.hora >= 24:
            self.clima = self.escolher_clima()
            self.hora = 0
            self.dia += 1
            self.log('')
            self.log(f'=============== Dia {self.dia} ===============')
            self.log('')
        
        self.atualizar_status_weather()


    def events(self):
        from random import choice, randint
        from modules.logica import verificar_resultado

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.MOUSEWHEEL:

                mouse_pos = pygame.mouse.get_pos()

                # 🔹 SOMENTE se o mouse estiver sobre o bloco de logs
                if self.logs_screen.collidepoint(mouse_pos):

                    padding = 10
                    line_height = 15

                    visible_height = self.logs_screen.height - padding * 2
                    total_height = len(self.logs) * line_height

                    max_scroll = max(0, total_height - visible_height)

                    self.scroll_offset -= event.y * 20
                    self.scroll_offset = max(0, min(self.scroll_offset, max_scroll))
                
                # 🔹 Scroll locais dominados
                for exercito_id, area in self.locais_area.items():
                    if area.collidepoint(mouse_pos):

                        total_height = len(self.army_card_cache[exercito_id]["locais"]) * 15
                        visible = area.height
                        max_scroll = max(0, total_height - visible)

                        self.locais_scroll[exercito_id] -= event.y * 15
                        self.locais_scroll[exercito_id] = max(
                            0,
                            min(self.locais_scroll[exercito_id], max_scroll)
                        )

       
            if event.type == self.UPDATE_EVENT:

                # sistema de chance
                if randint(1, 100) <= self.event_chance:

                    for exercito in self.exercitos_ativos:
                        exercito.marechal.character.set_mode("Idle")

                    index = self.exercito_index
                    exercito = self.exercitos_ativos[index]
                    print(self.guerra_ativa)
                    inimigo = choice(exercito.inimigos)

                    exercito.inimigo = inimigo
                    inimigo.inimigo = exercito

                    dado_especial1 = randint(1, 100)
                    dado_especial2 = randint(1, 100)

                    if dado_especial1 == dado_especial2:
                        self.evento_poder(exercito)
                    
                    else:
                        dado1 = randint(1, 100)
                        dado2 = randint(1, 100)

                        self.batalha(exercito, inimigo, dado1, dado2)
                    
                    numero_exercitos_ativos = len(self.exercitos_ativos)

                    exercito.territorio = len(exercito.tiles)
                    inimigo.territorio = len(inimigo.tiles)
                    
                    for agente in [exercito, inimigo]:
                        logs = verificar_resultado(
                            agente,
                            self
                        )

                        if logs:
                            for linha in logs:
                                self.log(linha)

                    self.atualizar_army_cards()

                    # reset da chance
                    self.event_chance = 5

                    # próximo exército
                    if index == numero_exercitos_ativos - 1:
                        self.exercito_index = 0
                    else:
                        # se algum exército foi removido
                        if len(self.exercitos_ativos) < numero_exercitos_ativos:
                            # se o removido estava antes do índice atual, ajusta
                            if index > len(self.exercitos_ativos) - 1:
                                self.exercito_index = 0
                            else:
                                self.exercito_index = index  # não incrementa, pois a lista já "andou"
                        else:
                            self.exercito_index += 1

                else:
                    # aumenta chance se não ocorreu evento
                    self.event_chance = min(self.event_chance + 5, 100)
    

    def batalha(self, exercito, inimigo, dado1, dado2):
        from math import ceil
        from modules.logica import gerar_evento
        
        relogio = f"{self.horario}"

        if dado1 > dado2:
            poder_do_round = ceil((dado1 - dado2) / 3)
            evento = gerar_evento(exercito, poder_do_round, self.clima[0])
            if evento.tipo not in ['melhoria', 'sorte']:
                exercito.marechal.character.set_mode("Combat 1h - Idle")
                inimigo.marechal.character.set_mode("Combat 1h - Idle")
                self.expandir_territorio(exercito, dominate=True)
            else:
                exercito.marechal.character.set_mode("Run")
            self.log(f"{relogio} {evento.descricao}")
            self.log(f"           {evento.positivo}")
            evento.efeito_pos()

        else:
            poder_do_round = ceil((dado2 - dado1) / 3)
            evento = gerar_evento(exercito, poder_do_round, self.clima[0])
            if poder_do_round == 0: poder_do_round += 1
            if evento.tipo not in ['melhoria', 'sorte']:
                exercito.marechal.character.set_mode("Combat 1h - Idle")
                inimigo.marechal.character.set_mode("Combat 1h - Idle")
                self.expandir_territorio(exercito.inimigo, dominate=True)
            else:
                exercito.marechal.character.set_mode("Run")
            self.log(f"{relogio} {evento.descricao}")
            self.log(f"           {evento.negativo}")
            evento.efeito_neg()
    
    def evento_poder(self, exercito):
        from modules.logica import poder

        exercito.marechal.character.set_mode("Run")
        evento = poder(exercito)
        exercito.poder += 1
        self.log(f"{self.horario} BREAKING NEWS: {evento}")


    def log(self, texto):
        padding = 10
        line_height = self.line_height

        log_area_width = self.logs_screen.width - padding * 2

        visible_height = self.logs_screen.height - padding * 2
        total_height = len(self.logs) * line_height
        max_scroll = max(0, total_height - visible_height)

        estava_no_fim = self.scroll_offset >= max_scroll - 5

        # 🔹 quebra o texto em linhas
        linhas = self.render_text_wrapped(
            texto,
            self.fontsJB[10],
            self.cores["amarelo"],
            log_area_width
        )

        # adiciona cada linha como um "log"
        for linha in linhas:
            self.logs.append(linha)

        # limite de histórico
        self.logs = self.logs[-300:]

        total_height = len(self.logs) * line_height
        max_scroll = max(0, total_height - visible_height)

        if estava_no_fim:
            self.scroll_offset = max_scroll


    def render_text_wrapped(self, text, font, color, max_width):
        """
        Quebra um texto em várias superfícies respeitando max_width
        Retorna uma lista de Surfaces (uma por linha)
        """
        words = text.split(" ")
        lines = []
        current_line = ""

        for word in words:
            test_line = current_line + word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line.rstrip())
                current_line = word + " "

        if current_line:
            lines.append(current_line.rstrip())

        # renderiza
        return [font.render(line, True, color) for line in lines]


    def generate_map_tiles(self):
        from modules.objetos.tile import Tile

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
        self.processar_explosoes_agendadas()
        self.update_explosoes()
        self.draw_efeito_clima()
        pygame.draw.rect(self.screen, self.cores["darkgreen"], self.map_position, 3)
        fps = int(self.clock.get_fps())
        fps_text = self.fontsJB[12].render(f"FPS: {fps}", True, (255,255,255))
        self.screen.blit(fps_text, (10,10))

        pygame.display.flip()
    
    #SPRITES DE EXPLOSAO#

    def sprite_explosao(self):
        for explosao in ['explosao1', 'explosao2']:
            arquivo = self.spritesheet[explosao]['arquivo']
            layer = self.spritesheet[explosao]['layer']
            self.spritesheet[explosao]['frames'] = [self.get_frame(arquivo, i, 64, 64, layer) for i in range(12)]
        self.explosoes = []
        self.explosoes_agendadas = []

    def update_explosoes(self):
        for explosao in self.explosoes:
            explosao.update()
            explosao.draw(self.screen)

        self.explosoes = [e for e in self.explosoes if not e.finished]
        self.explosoes = self.explosoes[-30:]

    def agendar_explosoes(self, x, y):
        from random import randint, choice

        if len(self.explosoes_agendadas) > 15:
            return

        agora = pygame.time.get_ticks()

        explosao_tipo = choice(['explosao1', 'explosao2'])

        for i in range(randint(5, 8)):
            delay = randint(200, 400) * i
            self.explosoes_agendadas.append({
                "tempo": agora + delay,
                "x": randint(x - 32, x - 12),
                "y": randint(y - 32, y - 12),
                "tipo": explosao_tipo
            })
    
    def processar_explosoes_agendadas(self):
        from modules.objetos.explosao import Explosao

        agora = pygame.time.get_ticks()

        for explosao in self.explosoes_agendadas[:]:

            if len(self.explosoes) >= 20:
                break

            if agora >= explosao["tempo"]:
                self.explosoes.append(
                    Explosao(
                        explosao["x"],
                        explosao["y"],
                        self.spritesheet[explosao["tipo"]]["frames"]
                    )
                )
                self.explosoes_agendadas.remove(explosao)


    def draw_day_weather_status(self):
        self.screen_day_weather_status = pygame.Rect(20, 20, 600, 60)
        pygame.draw.rect(self.screen, self.cores["secundaria"], self.screen_day_weather_status)
        pygame.draw.rect(self.screen, self.cores["darkgreen"], self.screen_day_weather_status, 3)

        self.screen.blit(self.renders["status_dia_texto"], (40, 30))

        cache = self.status_weather_cache

        self.screen.blit(cache["dia"], (110, 30))
        
        self.screen.blit(cache["clima"], (170, 35))
        clima_imagem_x = 170 + cache["clima"].get_width() + 10
        self.screen.blit(cache["clima_imagem"], (clima_imagem_x, 34))

        self.screen.blit(cache["horario"], (490, 30))


    def draw_army_cards(self):
        x_minimo = 20
        y_minimo = self.screen_day_weather_status.height + 40

        self.army_cards = {}

        for index, exercito in enumerate(self.exercitos):
            if index == 0:
                card = pygame.Rect(x_minimo, y_minimo, 290, 330)
                frame_marechal = pygame.Rect(x_minimo + 190, y_minimo + 10, 60, 90)
            elif index == 1:
                card = pygame.Rect(x_minimo + 310, y_minimo, 290, 330)
                frame_marechal = pygame.Rect(x_minimo + 190 + 310, y_minimo + 10, 60, 90)
            elif index == 2:
                card = pygame.Rect(x_minimo, y_minimo + 350, 290, 330)
                frame_marechal = pygame.Rect(x_minimo + 190, y_minimo + 10 + 350, 64, 90)
            elif index == 3:
                card = pygame.Rect(x_minimo + 310, y_minimo + 350, 290, 330)
                frame_marechal = pygame.Rect(x_minimo + 190 + 310, y_minimo + 10 + 350, 64, 90)

            pygame.draw.rect(self.screen, self.cores["secundaria"], card)
            pygame.draw.rect(self.screen, self.cores["darkgreen"], card, 3)

            pygame.draw.rect(self.screen, (200, 230, 200), frame_marechal)
            pygame.draw.rect(self.screen, self.cores["darkgreen"], frame_marechal, 3)
            exercito.marechal.character.update(self.dt)
            exercito.marechal.character.draw(self.screen, (frame_marechal.x, frame_marechal.y + 5))

            # --- Textos dentro do card ---
            cache = self.army_card_cache[exercito.id]

            self.screen.blit(cache["nome"], (card.x + 10, card.y + 10))
            self.screen.blit(cache["marechal"], (card.x + 10, card.y + 40))
            self.screen.blit(cache["perfil"], (card.x + 10, card.y + 60))
            self.screen.blit(cache["territorios"], (card.x + 10, card.y + 80))
            self.screen.blit(cache["poder"][0], (card.x + card.width - cache["poder"][1], card.y + 5))

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
            self.screen.blit(cache["locais_quantidade"], (card.x + 132, card.y + 185))

            # 🔹 Área visível dos locais dominados
            locais_area = pygame.Rect(
                card.x + 10,
                card.y + 205,
                card.width - 20,
                120
            )

            # salva a área
            self.locais_area[exercito.id] = locais_area

            # inicializa scroll se não existir
            if exercito.id not in self.locais_scroll:
                self.locais_scroll[exercito.id] = 0

            # ativa recorte
            self.screen.set_clip(locais_area)

            y = locais_area.y - self.locais_scroll[exercito.id]

            for local in cache["locais"]:
                self.screen.blit(local, (locais_area.x, y))
                y += 15

            self.screen.set_clip(None)
    

    def atualizar_status_weather(self):
        cache = {}

        cache["dia"] = self.fontsJB[28].render(f"{self.dia}", True, self.cores["amarelo"])

        cache["clima"] = self.fontsJB[24].render(f"{self.clima[0].title()}", True, self.cores["amarelo"])

        cache["clima_imagem"] = self.clima[1]

        cache["horario"] = self.fontsJB[28].render(self.horario_formatado, True, self.cores["amarelo"])

        self.status_weather_cache = cache
    

    def atualizar_army_cards(self):

        from modules.objetos.num_romano import numeros_romanos

        self.army_card_cache = {}

        for exercito in self.exercitos:
            cache = {}

            cache["nome"] = self.fontsJB[16].render(exercito.nome, True, exercito.cor)

            cache["marechal"] = self.fontsJB[12].render(
                f"Marechal {exercito.marechal.nome}",
                True,
                (200,200,200)
            )

            cache["perfil"] = self.fontsJB[12].render(
                exercito.marechal.perfil,
                True,
                exercito.marechal.cor
            )

            cache["poder"] = [self.fontDVS.render(
                numeros_romanos[exercito.poder][0],
                True,
                exercito.cor
            ), numeros_romanos[exercito.poder][1]]

            cache["territorios"] = self.fontsJB[12].render(
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
                    self.fontsJB[12].render(str(atributo), True, self.cores["branco"])
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
                    self.fontsJB[10].render(f"> {local[0]}", True, cor)
                )
            
            cache["locais_quantidade"] = self.fontsJB[12].render(
                f"{len(exercito.locais)}",
                True,
                self.cores["branco"]
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
        from modules.objetos.local import gerar_local
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
            locais = randint(5, 8)

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
                    if vizinho.dono is None:
                        tiles_disponiveis.add(vizinho)
                    elif dominate and vizinho.dono is exercito.inimigo:
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


    def atualizar_tile_visual(self, tile):
        x = tile.tile.x - self.map_position[0]
        y = tile.tile.y - self.map_position[1]

        # limpa o tile
        pygame.draw.rect(self.map_surface, (0,0,0,0), (x, y, 20, 20))

        overlay = self.army_overlays[tile.dono.id]
        self.map_surface.blit(overlay, (x, y))

        if tile.local and tile.local.tipo in self.local_icons:
            imagem = self.local_icons[tile.local.tipo]
            self.map_surface.blit(imagem, (x + 1, y + 1))
    

    def get_frame(self, sheet, frame, width, height, layer):
        rect = pygame.Rect(frame * width, layer * height, width, height)
        image = pygame.Surface((width, height), pygame.SRCALPHA)
        image.blit(sheet, (0, 0), rect)
        return image

if __name__ == "__main__":

    game = Game()
    game.run()
