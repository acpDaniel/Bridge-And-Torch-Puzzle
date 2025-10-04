from modelagem import Estado

class Dados:
    def __init__(self, tempos: dict[str, int]):
        self.tempos = tempos
        self.pessoas = set(tempos.keys())
        self.estado_inicial = Estado(grupo_inicio=self.pessoas, tocha_inicio=True)
        self.estado_final = Estado(grupo_inicio=set(), tocha_inicio=False)

    def __str__(self):
        pessoas = ", ".join(sorted(self.pessoas))
        return (
            f"Dados do Problema:\n"
            f"  Pessoas: {pessoas}\n"
            f"  Tempos: {self.tempos}\n"
            f"  Estado Inicial: {self.estado_inicial}\n"
            f"  Estado Final: {self.estado_final}\n"
        )
