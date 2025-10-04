from modelagem import Estado

def heuristica_soma_div2(estado: Estado, tempos: dict[str, int]) -> float:
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0.0
    return sum(tempos[p] for p in lado_inicio) / 2.0

def heuristica_maior_tempo_restante(estado: Estado, tempos: dict[str, int]) -> float:
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0.0
    return max(tempos[p] for p in lado_inicio)