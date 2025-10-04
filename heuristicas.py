from modelagem import Estado, TEMPOS

# Heurística: soma dos tempos de todos que ainda estão no lado inicial dividida por 2.
# Retorna uma estimativa admissível do tempo mínimo restante.
def heuristica_soma_div2(estado: Estado):
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0
    return sum(TEMPOS[p] for p in lado_inicio) / 2

# Heurística: tempo da pessoa mais lenta que ainda não atravessou.
# É admissível, pois no mínimo essa pessoa ainda precisará atravessar.
def heuristica_maior_tempo_restante(estado: Estado):
    lado_inicio = estado.grupo_inicio
    if not lado_inicio:
        return 0
    return max(TEMPOS[p] for p in lado_inicio)