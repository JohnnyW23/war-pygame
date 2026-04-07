class Evento:
    def __init__(self, exercito, tipo, descricao, positivo, efeito_pos, negativo, efeito_neg, consequencias=False, sprite_especial=False):
        self.exercito = exercito
        self.tipo = tipo
        self.descricao = descricao
        self.positivo = positivo
        self.efeito_pos = efeito_pos
        self.negativo = negativo
        self.efeito_neg = efeito_neg
        self.consequencias = consequencias
        self.sprite_especial = sprite_especial
