class Belly:
    """
    - reset(): Reinicia la panza (pepinos y tiempo).
    - comer(pepinos): Registra pepinos comidos (debe ser >= 0).
    - esperar(tiempo_en_horas): Aumenta el tiempo de espera.
    - esta_gruñendo(): Devuelve True si está gruñendo.
    """
    def __init__(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def reset(self):
        self.pepinos_comidos = 0
        self.tiempo_esperado = 0

    def comer(self, pepinos):
        if pepinos < 0:
            raise ValueError("No se permite una cantidad negativa de pepinos")
        self.pepinos_comidos += pepinos

    def esperar(self, tiempo_en_horas):
        if tiempo_en_horas > 0:
            self.tiempo_esperado += tiempo_en_horas

    def esta_gruñendo(self):
        return self.tiempo_esperado >= 1.5 and self.pepinos_comidos > 10

