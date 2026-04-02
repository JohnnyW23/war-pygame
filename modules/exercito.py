class Exercito:
    def __init__(self, id, nome, cor, canal_nome, canal_sigla):
        from random import uniform

        self.id = id
        self.nome = nome
        self.cor = cor
        self.poder = 1
        self.forca = 300
        self.tecnologia = 150
        self.suprimentos = 150
        self.moral = 150
        self.estrategia = 150
        self.inimigos = []
        self.tiles = []

        self.canal_nome = canal_nome
        self.canal_sigla = canal_sigla

        self.resumo = {
            "pib": round(uniform(0.1, 1), 2),
            "inflacao": round(uniform(1, 3), 2)
        }

        self.marechal = self.escolher_marechal()


    def escolher_marechal(self):
        from modules.marechal import Marechal
        import json
        from random import choice

        with open("war pygame/names.json", "r", encoding="utf-8") as f:
            names = json.load(f)
        
        marechais = [name['name'] for name in names if name['gender'] == 'male' or name['gender'] == 'unisex']

        perfis = [
            ["Agressivo", (255, 165, 0)],        # orange1
            ["Cauteloso", (0, 191, 255)],        # bright_blue
            ["Equilibrado", (105, 105, 105)],    # bright_black (cinza escuro)
            ["Oportunista", (255, 215, 0)],      # gold1
            ["Arrogante", (255, 0, 255)],        # magenta1
            ["Estrategista", (138, 43, 226)],    # blue_violet
            ["Sanguinário", (255, 0, 0)],        # red1
            ["Político", (127, 255, 0)],         # chartreuse1
            ["Instável", (139, 0, 0)]            # dark_red
        ]

        """
        equilibrado: nada acontece
        agressivo: 2x mais dano dado e 2x mais dano recebido
        cauteloso: 0.5x dano dado e 0.5x dano recebido
        oportunista: se a diferença dos dados for grande atacando, dá mais dano, mas se for pequena atacando, dá menos dano
        arrogante: se estiver ganhando por muita diferença, recebe mais dano, e se estiver perdendo por muita diferença, recebe menos dano
        estrategista: se estiver ganhando, dá menos dano, se estiver perdendo, dá mais dano
        sanguinario: vitórias seguidas dão um bonus acumulativo. derrotas seguidas são o mesmo bonus acumulativo
        politico: mais chance do inimigo se render
        instavel: pequena chance de converter vitórias em derrotas, e vice versa (esse terá informação inclusive caso seja ativado)
        """

        nome = choice(marechais)
        perfil_info = choice(perfis)
        cor = perfil_info[1]
        perfil = perfil_info[0]

        return Marechal(nome, perfil, cor)