class Local:
    def __init__(self, nome, tipo, raridade, bonus):
        self.nome = nome
        self.tipo = tipo
        self.raridade = raridade
        self.bonus = bonus
        self.bonus_label = self.gerar_label()
        self.cor = self.gerar_cor()
    

    def definir_bonus(self):
        from random import randint

        if self.raridade == "comum":
            return randint(1, 2)
        elif self.raridade == "incomum":
            return randint(2, 3)
        elif self.raridade == "raro":
            return randint(3, 4)
    

    def gerar_bonus(self, a):
        from random import random
        if random() < 0.4:
            bonus_value = self.definir_bonus()
            if self.bonus == "forca":
                a.forca += bonus_value
            elif self.bonus == "tecnologia":
                a.tecnologia += bonus_value
            elif self.bonus == "suprimentos":
                a.suprimentos += bonus_value
            elif self.bonus == "moral":
                a.moral += bonus_value
            elif self.bonus == "estrategia":
                a.estrategia += bonus_value


    def gerar_cor(self):
        if self.raridade == "comum":
            cor = (0, 255, 51)
        elif self.raridade == "incomum":
            cor = (0, 205, 255)
        elif self.raridade == "raro":
            cor = (245, 200, 20)
        
        return cor
    
    def gerar_label(self):
        if self.raridade == "comum":
            return f"{self.bonus} +"
        elif self.raridade == "incomum":
            return f"{self.bonus} ++"
        elif self.raridade == "raro":
            return f"{self.bonus} +++"


def gerar_local():
    from random import choices, choice

    chances= {
        "comum": 0.6,
        "incomum": 0.3,
        "raro": 0.1
    }

    tipos = {
        "comum": {
            "hospital": {
                "nome": ["Hospital", "Clínica", "Centro Médico", "Posto de Atendimento"],
                "nome complementar": [
                    "Central",
                    "Regional",
                    "Santa Maria",
                    "dos Anjos",
                    "de Campanha",
                    "Cruz Vermelha",
                    "São Lucas",
                    "São Rafael",
                    "dos Lírios",
                    "das Flores"
                ],
                "bonus": ["suprimentos", "moral"]
            },

            "militar": {
                "nome": ["Base Militar", "Quartel", "Instalação Militar", "Campo de Treinamento"],
                "nome complementar": [
                    "Central",
                    "de Estratégia",
                    "de Combate",
                    "de Apoio",
                    "de Logística",
                    "de Suprimentos",
                    "de Defesa",
                    "de Ataque",
                    "de Reconhecimento",
                    "de Operações"
                ],
                "bonus": ["forca", "moral", "estrategia"]
            },

            "fabrica": {
                "nome": ["Fábrica", "Complexo Industrial", "Usina", "Planta de Produção", "Centro de Manufatura", "Parque Industrial"],
                "nome complementar": [
                    "Nacional",
                    "Metalúrgica",
                    "de Produção",
                    "de Energia",
                    "de Armamento",
                    "de Suprimentos",
                    "de Combate",
                    "de Apoio",
                    "de Logística",
                    "de Tecnologia"
                ],
                "bonus": ["suprimentos", "tecnologia"]
            },

            "cidade": {
                "nome": ["Cidade", "Município", "Distrito Urbano", "Polo Urbano", "Metrópole", "Vila", "Aldeia"],
                "nome complementar": [
                    "Central",
                    "dos Portos",
                    "das Indústrias",
                    "das Comunicações",
                    "das Forças Armadas",
                    "da Vitória",
                    "da Liberdade",
                    "da Paz",
                    "da Esperança",
                    "da União",
                    "da Fraternidade",
                    "da Justiça",
                    "Secular"
                ],
                "bonus": ["moral", "suprimentos", "tecnologia"]
            },

            "porto": {
                "nome": ["Porto", "Terminal Naval", "Doca", "Base Naval", "Complexo Portuário","Marina", "Estação Marítima"],
                "nome complementar": [
                    "Comercial",
                    "Estratégico",
                    "Internacional",
                    "Militar",
                    "de Carga",
                    "de Passageiros",
                    "de Pesca",
                    "de Contêineres",
                    "de Suprimentos",
                    "de Combate",
                    "de Apoio",
                    "dos Sete Mares"
                ],
                "bonus": ["suprimentos", "estrategia"]
            },

            "aeroporto": {
                "nome": ["Aeroporto", "Base Aérea", "Aeródromo", "Heliporto", "Campo de Aviação", "Terminal Aéreo"],
                "nome complementar": [
                    "Internacional",
                    "Militar",
                    "Regional",
                    "Central",
                    "de Carga",
                    "de Passageiros",
                    "de Suprimentos",
                    "de Combate",
                    "de Apoio",
                    "Nacional",
                    "Federal"
                ],
                "bonus": ["tecnologia", "estrategia"]
            },

            "base de misseis": {
                "nome": ["Base de Mísseis", "Complexo de Mísseis", "Instalação de Mísseis", "Campo de Mísseis"],
                "nome complementar": [
                    "Nacional",
                    "Federal",
                    "de Defesa",
                    "de Ataque",
                    "de Longo Alcance",
                    "de Curto Alcance",
                    "Balísticos",
                    "de Cruzeiro",
                    "Hipersônicos"
                ],
                "bonus": ["forca", "tecnologia"]
            },

            "centro comercial": {
                "nome": ["Centro Comercial", "Distrito Comercial", "Zona de Comércio", "Polo Comercial", "Área de Negócio"],
                "nome complementar": [
                    "de Importação",
                    "de Exportação",
                    "de Logística",
                    "de Suprimentos",
                    "de Combate",
                    "de Apoio",
                    "de Tecnologia",
                    "Nacional",
                    "Federal",
                    "Internocional"
                ],
                "bonus": ["suprimentos", "tecnologia"]
            }
        },

        "incomum": {
            "centro de pesquisa": {
                "nome": ["Centro de Pesquisa", "Instituto Tecnológico", "Laboratório", "Complexo Científico", "Polo Científico", "Parque Tecnológico"],
                "nome complementar": [
                    "Avançado",
                    "Experimental",
                    "Nacional",
                    "de Inovação",
                    "de Desenvolvimento",
                    "de Microprocessadores",
                    "de I.A.",
                    "de Robótica",
                    "de Biotecnologia",
                    "de Energia",
                    "de Biologia",
                    "de Nanotecnologia"
                ],
                "bonus": ["tecnologia", "estrategia"]
            },

            "arsenal": {
                "nome": ["Arsenal", "Depósito de Armas", "Complexo Bélico", "Base de Armamento", "Fábrica de Armamento", "Parque de Armamento"],
                "nome complementar": [
                    "Central",
                    "Federal",
                    "Subterrâneo",
                    "Secreto",
                    "Nacional",
                    "Nuclear",
                    "Químico",
                    "Biológico",
                    "Convencional"
                ],
                "bonus": ["forca", "suprimentos"]
            },

            "central comunicacoes": {
                "nome": ["Centro de Comunicações", "Centro de Transmissão", "Estação de Rádio", "Complexo de Comunicações", "Base de Comunicações", "Parque de Comunicações"],
                "nome complementar": [
                    "de Estratégia",
                    "Nacional",
                    "Central",
                    "de Operações",
                    "de Inteligência",
                    "de Guerra Eletrônica",
                    "de Interceptação",
                    "de Propaganda",
                    "de Cibersegurança"
                ],
                "bonus": ["estrategia", "moral"]
            },

            "refinaria": {
                "nome": ["Refinaria", "Planta Energética", "Complexo de Combustíveis", "Base de Energia", "Fábrica de Combustíveis", "Parque Energético"],
                "nome complementar": [
                    "Nacional",
                    "Industrial",
                    "de Petróleo",
                    "de Gás",
                    "de Combate",
                    "de Apoio",
                    "de Logística"
                ],
                "bonus": ["suprimentos", "tecnologia"]
            },

            "academia militar": {
                "nome": ["Academia Militar", "Escola de Oficiais", "Instituto de Formação", "Centro Avançado", "Colégio Militar"],
                "nome complementar": [
                    "Superior",
                    "de Guerra",
                    "de Estratégia",
                    "de Combate",
                    "de Apoio",
                    "de Logística",
                    "de Inteligência",
                    "de Operações",
                    "de Defesa",
                    "Nacional",
                    "Federal"
                ],
                "bonus": ["moral", "estrategia"]
            },

            "centro logistico": {
                "nome": ["Centro Logístico", "Entreposto Militar", "Complexo de Suprimentos", "Base de Apoio Logístico", "Parque de Suprimentos"],
                "nome complementar": [
                    "Avançado",
                    "Central",
                    "Nacional",
                    "Federal",
                    "de Combate",
                    "de Apoio"
                ],
                "bonus": ["suprimentos"]
            },

            "museu": {
                "nome": ["Museu", "Memorial", "Instituto", "Centro de Patrimônio", "Arquivo", "Biblioteca do Marco", "Galeria do Saber"],
                "nome complementar": [
                    "Histórico",
                    "Cultural",
                    "de Arte",
                    "de Música",
                    "de Ciência",
                    "Nacional",
                    "Federal",
                    "da Independência"
                ],
                "bonus": ["tecnologia"]
            },

            "monumento": {
                "nome": ["Flor", "Coleiro", "A Videira", "Mares", "O Pilar", "O Farol", "Homem", "Mulher", "O Guerreiro", "A Guerreira", "O Defensor", "A Defensora", "Cavalo", "Serpente", "Águia", "Leão", "Dragão", "Fênix"],
                "nome complementar": [
                    "da Independência",
                    "da Vitória",
                    "da Liberdade",
                    "da Paz",
                    "da Esperança",
                    "da União",
                    "da Nação",
                    "dos Caídos",
                    "dos Heróis",
                    "dos Deuses",
                    "da Justiça",
                    "Secular",
                    "da Eternidade",
                    "do Infinito",
                    "da Glória",
                    "da Honra",
                    "da Coragem",
                    "da Força",
                    "da Sabedoria"
                ],
                "bonus": ["moral"]
            }
        },

        "raro": {
            "quartel general": {
                "nome": ["Quartel-General", "Comando Supremo", "Sede do Comando", "Centro de Comando", "Ninho da Águia", "Fortaleza"],
                "nome complementar": [
                    "Central",
                    "do Marechal",
                    "do General",
                    "do Capitão",
                    "de Combate",
                    "de Apoio",
                    "de Logística",
                    "de Inteligência",
                    "de Operações Especiais",
                    "Nacional",
                    "Federal"
                ],
                "bonus": ["estrategia", "moral"]
            },

            "capital": {
                "nome": ["Capital", "Sede do Governo", "Centro Político"],
                "nome complementar": [
                    "Nacional",
                    "Federal",
                    "da Independência",
                    "da Vitória",
                    "da Liberdade",
                    "da Paz",
                    "da Esperança",
                    "da União",
                    "da Fraternidade",
                    "da Justiça",
                    "Secular"
                ],
                "bonus": ["moral", "estrategia", "forca"]
            },

            "complexo secreto": {
                "nome": ["Complexo Secreto", "Ninho da Serpente", "O Abismo", "O Labirinto"],
                "nome complementar": [
                    "Oculto",
                    "Classificado",
                    "Subterrâneo",
                    "Secreto",
                    "Nacional",
                    "Federal",
                    "de Combate",
                    "de Apoio",
                    "do Segredo",
                    "de Espionagem",
                    "de Inteligência"
                ],
                "bonus": ["tecnologia", "estrategia"]
            },

            "marco simbolico": {
                "nome": ["Santuário", "Marco Histórico", "Símbolo", "Campo", "Memorial", "Altar", "Pilar", "Farol"],
                "nome complementar": [
                    "da Independência",
                    "da Vitória",
                    "da Liberdade",
                    "da Paz",
                    "da Esperança",
                    "da União",
                    "da Nação",
                    "dos Caídos",
                    "dos Heróis",
                    "dos Deuses",
                    "da Justiça"
                ],
                "bonus": ["moral"]
            }
        }
    }

    raridade = choices(list(chances.keys()), weights=list(chances.values()), k=1)[0]
    categoria = choices(list(tipos[raridade].keys()), k=1)[0]
    nome = f"{choices(tipos[raridade][categoria]['nome'], k=1)[0]} {choices(tipos[raridade][categoria]['nome complementar'], k=1)[0]}"
    bonus = choice(tipos[raridade][categoria]['bonus'])

    return Local(nome, categoria, raridade, bonus)