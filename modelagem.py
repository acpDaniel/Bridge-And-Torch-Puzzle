import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations


# ===============================================================================================
# Classe Estado
# ===============================================================================================

class Estado:
    def __init__(self, grupo_inicio: set, tocha_inicio: bool):
        self.grupo_inicio = grupo_inicio
        self.tocha_inicio = tocha_inicio

    def __str__(self):
        grupo_ordenado = ", ".join(sorted(self.grupo_inicio))
        return f"{{{grupo_ordenado}}} {'inicio' if self.tocha_inicio else 'final'}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, outro):
        return (self.grupo_inicio == outro.grupo_inicio
                and self.tocha_inicio == outro.tocha_inicio)

    def __hash__(self):
        return hash((frozenset(self.grupo_inicio), self.tocha_inicio))


# ===============================================================================================
# Classe Grafo
# ===============================================================================================

class Grafo:
    def __init__(self):
        # dicionário: {rótulo_estado: {vizinho: custo}}
        self.lista_adjacencia = {}

    def adicionar_estado(self, estado: Estado):
        rotulo = str(estado)
        if rotulo not in self.lista_adjacencia:
            self.lista_adjacencia[rotulo] = {}

    def adicionar_aresta(self, estado1: Estado, estado2: Estado, custo: int):
        rot1, rot2 = str(estado1), str(estado2)
        for rot in [rot1, rot2]:
            if rot not in self.lista_adjacencia:
                self.adicionar_estado(rot)
        self.lista_adjacencia[rot1][rot2] = custo

    def show(self, titulo="Algoritmo", descricao=""):
        G = nx.DiGraph()
        for v1, vizinhos in self.lista_adjacencia.items():
            for v2, custo in vizinhos.items():
                G.add_edge(v1, v2, weight=custo)

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, seed=40, k=1)
        nx.draw(G, pos, with_labels=True, node_size=2000,
                node_color="lightblue", font_size=12)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title(titulo, fontsize=20)
        plt.text(-0.2, 0.5, descricao, fontsize=14, ha='left', va='center',
                 transform=plt.gca().transAxes)
        plt.show(block=True)


# ===============================================================================================
# Classe Passo
# ===============================================================================================

class Passo:
    def __init__(self, estado_origem: Estado, estado_destino: Estado,
                 grupo_viajante: set, custo: int):
        self.estado_origem = estado_origem
        self.estado_destino = estado_destino
        self.grupo_viajante = grupo_viajante
        self.custo = custo

    def __str__(self):
        grupo = ", ".join(sorted(self.grupo_viajante))
        return f"→ {self.estado_destino}; Passageiros: {{{grupo}}}; Custo: {self.custo}"

    def __repr__(self):
        return f"Passo({self.estado_origem} -> {self.estado_destino}, {self.grupo_viajante}, {self.custo})"


# ===============================================================================================
# Funções de geração de sucessores
# ===============================================================================================

def gerar_grupos_viajantes(grupo_pessoas: set):
    """Gera subconjuntos de 1 ou 2 pessoas para atravessar a ponte."""
    for combination in combinations(grupo_pessoas, 1):
        yield set(combination)
    for combination in combinations(grupo_pessoas, 2):
        yield set(combination)


def funcao_sucessora(estado: Estado, tempos: dict[str, int], pessoas: set) -> list[Passo]:
    """Gera todos os passos possíveis a partir de um estado dado os tempos e pessoas."""
    possiveis_passos = []

    if estado.tocha_inicio:
        # Movimento: esquerda → direita
        for grupo_viajante in gerar_grupos_viajantes(estado.grupo_inicio):
            novo_grupo_inicio = estado.grupo_inicio - grupo_viajante
            estado_sucessor = Estado(grupo_inicio=novo_grupo_inicio, tocha_inicio=False)
            custo = max(tempos[p] for p in grupo_viajante)
            possiveis_passos.append(
                Passo(estado, estado_sucessor, grupo_viajante, custo)
            )
    else:
        # Movimento: direita → esquerda
        grupo_fim = pessoas - estado.grupo_inicio
        for grupo_viajante in gerar_grupos_viajantes(grupo_fim):
            novo_grupo_inicio = estado.grupo_inicio | grupo_viajante
            estado_sucessor = Estado(grupo_inicio=novo_grupo_inicio, tocha_inicio=True)
            custo = max(tempos[p] for p in grupo_viajante)
            possiveis_passos.append(
                Passo(estado, estado_sucessor, grupo_viajante, custo)
            )

    return possiveis_passos
