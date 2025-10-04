import heapq
from time import time
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt
from modelagem import Estado, funcao_sucessora


# ===============================================================================================
# Classe Base
# ===============================================================================================

SEED = 42

class AlgoritmoBusca:
    def __init__(self, dados, nome="Algoritmo"):
        self.dados = dados
        self.nome = nome
        self.caminho = []
        self.custo_total = None
        self.tempo_exec = None
        self.nos_expandidos = 0
        self.visitados = set()
        self.expandidos = []
        self._global_pos = None

    def solve(self):
        raise NotImplementedError()

    def _gerar_grafo_completo(self):
        pessoas = sorted(self.dados.pessoas)
        n = len(pessoas)
        total_estados = 2 ** (n + 1)
        G = nx.DiGraph()
        for bits in range(total_estados):
            tocha_bit = bits & 1
            pessoa_bits = bits >> 1
            grupo_inicio = {p for i, p in enumerate(pessoas) if not (pessoa_bits & (1 << i))}
            estado = Estado(grupo_inicio, not bool(tocha_bit))
            for passo in funcao_sucessora(estado, self.dados.tempos, self.dados.pessoas):
                G.add_edge(str(estado), str(passo.estado_destino), weight=passo.custo)
        return G

    def plot(self, view="global", expansions=False, ax=None):
        if view not in ("global", "path"):
            raise ValueError("view deve ser 'global' ou 'path'.")

        if view == "global":
            G = self._gerar_grafo_completo()
            pos = nx.spring_layout(G, seed=SEED, k=1.2)
            self._global_pos = pos
        else:
            G = nx.DiGraph()
            for passo in self.caminho:
                G.add_edge(str(passo.estado_origem), str(passo.estado_destino), weight=passo.custo)
            if expansions:
                for e in self.expandidos:
                    G.add_node(str(e))
            if getattr(self, "_global_pos", None):
                pos = {n: self._global_pos.get(n, None) for n in G.nodes()}
                faltantes = [n for n, p in pos.items() if p is None]
                if faltantes:
                    pos_local = nx.spring_layout(G.subgraph(faltantes), seed=SEED, k=1.2)
                    for n in faltantes:
                        pos[n] = pos_local[n]
            else:
                pos = nx.spring_layout(G, seed=SEED, k=1.2)

        if ax is None:
            _, ax = plt.subplots(figsize=(18, 12))

        expandidos_str = {str(e) for e in self.expandidos}
        caminho_nodes = {str(passo.estado_origem) for passo in self.caminho} | {str(passo.estado_destino) for passo in self.caminho}

        cores = []
        for n in G.nodes():
            if n in caminho_nodes:
                cores.append("skyblue")
            elif expansions and n in expandidos_str:
                cores.append("orange")
            else:
                cores.append("lightgray")

        caminho_edges = {(str(passo.estado_origem), str(passo.estado_destino)) for passo in self.caminho}

        nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1, ax=ax)
        nx.draw_networkx_edges(G, pos, edgelist=caminho_edges, edge_color="red", width=2.5, ax=ax)
        nx.draw(G, pos, node_color=cores, with_labels=True, node_size=800, font_size=8, ax=ax)

        edge_labels = nx.get_edge_attributes(G, 'weight')
        nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8, font_color='black', ax=ax)

        ax.set_title(f"{self.nome} — {'Grafo completo' if view=='global' else 'Caminho ótimo'}"
                     f"{' (expandidos destacados)' if expansions else ''}", fontsize=16)

        
# ===============================================================================================
# BFS
# ===============================================================================================

class BFS(AlgoritmoBusca):
    def __init__(self, dados):
        super().__init__(dados, nome="BFS")

    def solve(self):
        inicio = time()
        estado_inicial = self.dados.estado_inicial
        estado_objetivo = self.dados.estado_final
        visitados = set([estado_inicial])
        fila = deque([(estado_inicial, [], 0)])
        nos_expandidos = 0
        expandidos = []

        while fila:
            estado_atual, caminho, custo_atual = fila.popleft()
            expandidos.append(estado_atual)
            nos_expandidos += 1

            for passo in funcao_sucessora(estado_atual, self.dados.tempos, self.dados.pessoas):
                if passo.estado_destino.grupo_inicio == estado_objetivo.grupo_inicio:
                    fim = time()
                    self.caminho = caminho + [passo]
                    self.custo_total = custo_atual + passo.custo
                    self.tempo_exec = fim - inicio
                    self.nos_expandidos = nos_expandidos
                    self.visitados = visitados
                    self.expandidos = expandidos
                    return

                if passo.estado_destino not in visitados:
                    visitados.add(passo.estado_destino)
                    fila.append((passo.estado_destino, caminho + [passo], custo_atual + passo.custo))

        fim = time()
        self.tempo_exec = fim - inicio
        self.nos_expandidos = nos_expandidos
        self.visitados = visitados
        self.expandidos = expandidos


# ===============================================================================================
# DFS
# ===============================================================================================

class DFS(AlgoritmoBusca):
    def __init__(self, dados, limite=10_000):
        super().__init__(dados, nome="DFS")
        self.limite = limite

    def solve(self):
        inicio = time()
        estado_inicial = self.dados.estado_inicial
        estado_objetivo = self.dados.estado_final
        visitados = set()
        pilha = [(estado_inicial, [], 0)]
        nos_expandidos = 0
        expandidos = []

        while pilha and nos_expandidos < self.limite:
            estado_atual, caminho, custo_atual = pilha.pop()
            if estado_atual in visitados:
                continue
            visitados.add(estado_atual)
            expandidos.append(estado_atual)
            nos_expandidos += 1

            if estado_atual == estado_objetivo:
                fim = time()
                self.caminho = caminho
                self.custo_total = custo_atual
                self.tempo_exec = fim - inicio
                self.nos_expandidos = nos_expandidos
                self.visitados = visitados
                self.expandidos = expandidos
                return

            for passo in funcao_sucessora(estado_atual, self.dados.tempos, self.dados.pessoas):
                pilha.append((passo.estado_destino, caminho + [passo], custo_atual + passo.custo))

        fim = time()
        self.tempo_exec = fim - inicio
        self.nos_expandidos = nos_expandidos
        self.visitados = visitados
        self.expandidos = expandidos


# ===============================================================================================
# Custo Uniforme
# ===============================================================================================

class CustoUniforme(AlgoritmoBusca):
    def __init__(self, dados):
        super().__init__(dados, nome="Custo Uniforme")

    def solve(self):
        inicio = time()
        estado_inicial = self.dados.estado_inicial
        estado_objetivo = self.dados.estado_final
        melhor_custo = {estado_inicial: 0}
        heap = []
        contador = 0
        heapq.heappush(heap, (0, contador, estado_inicial, []))
        nos_expandidos = 0
        expandidos = []

        while heap:
            custo_atual, _, estado_atual, caminho = heapq.heappop(heap)
            expandidos.append(estado_atual)
            nos_expandidos += 1

            if custo_atual > melhor_custo.get(estado_atual, float('inf')):
                continue

            if estado_atual == estado_objetivo:
                fim = time()
                self.caminho = caminho
                self.custo_total = custo_atual
                self.tempo_exec = fim - inicio
                self.nos_expandidos = nos_expandidos
                self.expandidos = expandidos
                return

            for passo in funcao_sucessora(estado_atual, self.dados.tempos, self.dados.pessoas):
                estado_sucessor = passo.estado_destino
                novo_custo = custo_atual + passo.custo

                if novo_custo < melhor_custo.get(estado_sucessor, float('inf')):
                    melhor_custo[estado_sucessor] = novo_custo
                    contador += 1
                    heapq.heappush(heap, (novo_custo, contador, estado_sucessor, caminho + [passo]))

        fim = time()
        self.tempo_exec = fim - inicio
        self.nos_expandidos = nos_expandidos
        self.expandidos = expandidos


# ===============================================================================================
# A*
# ===============================================================================================

class AEstrela(AlgoritmoBusca):
    def __init__(self, dados, funcao_heuristica):
        super().__init__(dados, nome="A*")
        self.funcao_heuristica = funcao_heuristica

    def solve(self):
        inicio = time()
        estado_inicial = self.dados.estado_inicial
        estado_objetivo = self.dados.estado_final
        melhor_custo = {estado_inicial: 0}
        heap = []
        contador = 0

        f0 = self.funcao_heuristica(estado_inicial, self.dados.tempos)
        heapq.heappush(heap, (f0, contador, 0, estado_inicial, []))

        nos_expandidos = 0
        expandidos = []

        while heap:
            f_atual, _, g_atual, estado_atual, caminho = heapq.heappop(heap)
            expandidos.append(estado_atual)
            nos_expandidos += 1

            if estado_atual == estado_objetivo:
                fim = time()
                self.caminho = caminho
                self.custo_total = g_atual
                self.tempo_exec = fim - inicio
                self.nos_expandidos = nos_expandidos
                self.expandidos = expandidos
                return

            if g_atual > melhor_custo.get(estado_atual, float('inf')):
                continue

            for passo in funcao_sucessora(estado_atual, self.dados.tempos, self.dados.pessoas):
                estado_sucessor = passo.estado_destino
                g_novo = g_atual + passo.custo

                f_novo = g_novo + self.funcao_heuristica(estado_sucessor, self.dados.tempos)

                if g_novo < melhor_custo.get(estado_sucessor, float('inf')):
                    melhor_custo[estado_sucessor] = g_novo
                    contador += 1
                    heapq.heappush(heap, (f_novo, contador, g_novo, estado_sucessor, caminho + [passo]))

        fim = time()
        self.tempo_exec = fim - inicio
        self.nos_expandidos = nos_expandidos
        self.expandidos = expandidos
