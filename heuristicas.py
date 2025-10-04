from modelagem import Estado


# ===============================================================================================
# Heurística: soma dos tempos de todos que ainda estão no lado inicial dividida por 2.
# Retorna uma estimativa admissível do tempo mínimo restante.
# ===============================================================================================
def heuristica_soma_div2(estado: Estado, tempos: dict[str, int]) -> float:
    """
    Estima o tempo restante como metade da soma dos tempos
    das pessoas que ainda estão no lado inicial.
    """
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0.0
    return sum(tempos[p] for p in lado_inicio) / 2.0


# ===============================================================================================
# Heurística: tempo da pessoa mais lenta que ainda não atravessou.
# É admissível, pois no mínimo essa pessoa ainda precisará atravessar.
# ===============================================================================================
def heuristica_maior_tempo_restante(estado: Estado, tempos: dict[str, int]) -> float:
    """
    Estima o tempo restante pelo tempo da pessoa mais lenta
    que ainda está no lado inicial.
    """
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0.0
    return max(tempos[p] for p in lado_inicio)
