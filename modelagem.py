import networkx as nx
import matplotlib.pyplot as plt
from itertools import combinations, chain

TEMPOS = {'A': 1, 'B': 2, 'C': 5, 'D': 10}
PESSOAS = set(TEMPOS.keys())

class Estado:
    grupo_inicio : set
    tocha_inicio : bool
    def __init__(self, grupo_inicio : set, tocha_inicio : bool):
        self.grupo_inicio = grupo_inicio
        self.tocha_inicio = tocha_inicio

    # Necessário para printar a classe, e também necessário para fazer o typecast str() do Estado na hora de 'nomear' os vértices do grafo
    def __str__(self):
        self.grupo_inicio
        grupo_inicio_ordenado = ", ".join(str(p) for p in sorted(self.grupo_inicio))
        return f"{{{grupo_inicio_ordenado}}} {'inicio' if self.tocha_inicio else 'final'}"

    # Ajuda no print também
    def __repr__(self):
        return self.__str__()

    # Necessário para comparar as estruturas quando se roda os algoritmos, para questões de prioridade nas E.Ds e etc
    def __eq__(self, outro):
        return (self.grupo_inicio == outro.grupo_inicio and
                self.tocha_inicio == outro.tocha_inicio)

    # Permite usar Estado em sets e dicts
    def __hash__(self):
        return hash((frozenset(self.grupo_inicio), self.tocha_inicio))
    

class Grafo:
    def __init__(self):
        # É um dicionário onde cada chave é um estado
        # e o valor é outro dicionário com {estado_vizinho: custo}
        self.lista_adjacencia = {}

    def adicionar_estado(self, estado : Estado):
        rotulo_vertice = str(estado)

        if rotulo_vertice not in self.lista_adjacencia:
            self.lista_adjacencia[rotulo_vertice] = {}
    
    def adicionar_aresta(self, estado1 : Estado, estado2 : Estado, custo : int):
        rotulo_vertice1 = str(estado1)
        rotulo_vertice2 = str(estado2)
            
        for rotulo in [rotulo_vertice1, rotulo_vertice2]:
            if rotulo not in self.lista_adjacencia:
                self.adicionar_estado(rotulo)
        self.lista_adjacencia[rotulo_vertice1][rotulo_vertice2] = custo

    def show(self, titulo="Algoritmo", descricao=""):
        G = nx.DiGraph()
        for v1, vizinhos in self.lista_adjacencia.items():
            for v2, custo in vizinhos.items():
                G.add_edge(v1, v2, weight=custo)

        plt.figure(figsize=(15, 10))
        pos = nx.spring_layout(G, seed=40,k=1)
        nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12)
        labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        plt.title(titulo, fontsize=20)
        plt.text(-0.2, 0.5, descricao, fontsize=14, ha='left', va='center', transform=plt.gca().transAxes)
        plt.show(block=True)

class Passo:
    def __init__(self, estado_origem, estado_destino, grupo_viajante, custo):
        self.estado_origem = estado_origem
        self.estado_destino = estado_destino
        self.grupo_viajante = grupo_viajante
        self.custo = custo

    def __str__(self):
        grupo_passageiros = ", ".join(str(p) for p in sorted(self.grupo_viajante))
        return f"Estado destino: {self.estado_destino}; Passageiros: {{{grupo_passageiros}}}; Custo: {self.custo}"

    def __repr__(self):
        return f"Passo({self.estado_origem} -> {self.estado_destino}, {self.grupo_viajante}, {self.custo})"

# Gera todos os grupos possíveis de viajantes
# Usado para definir quem pode atravessar a ponte em um passo
# Exemplo: se grupo_pessoas = {"A", "B", "C"}, retorna:
# {"A"}, {"B"}, {"C"}, {"A","B"}, {"A","C"}, {"B","C"}
def gerar_grupos_viajantes(grupo_pessoas: set):
    casos_pessoa_isolada = (set(combination) for combination in combinations(grupo_pessoas, 1))
    casos_dupla = (set(combination) for combination in combinations(grupo_pessoas, 2))
    return chain(casos_pessoa_isolada, casos_dupla)


def funcao_sucessora(estado : Estado) -> list[Passo]:
    possiveis_passos = []

    if estado.tocha_inicio:
        for grupo_viajante in gerar_grupos_viajantes(estado.grupo_inicio):
            novo_grupo_inicio = estado.grupo_inicio - grupo_viajante
            estado_sucessor = Estado(grupo_inicio=novo_grupo_inicio, tocha_inicio=False)
            custo = max(map(TEMPOS.get, grupo_viajante))
            possiveis_passos.append(Passo(estado_origem=estado, estado_destino=estado_sucessor, grupo_viajante=grupo_viajante, custo=custo))
    else:
        grupo_fim = PESSOAS - estado.grupo_inicio
        for grupo_viajante in gerar_grupos_viajantes(grupo_fim):
            novo_grupo_inicio = estado.grupo_inicio | grupo_viajante
            estado_sucessor = Estado(grupo_inicio=novo_grupo_inicio, tocha_inicio=True)
            custo = max(map(TEMPOS.get, grupo_viajante))
            possiveis_passos.append(Passo(estado_origem=estado, estado_destino=estado_sucessor, grupo_viajante=grupo_viajante, custo=custo))

    return possiveis_passos