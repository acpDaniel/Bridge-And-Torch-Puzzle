import networkx as nx
import matplotlib.pyplot as plt
from matplotlib import colormaps
from modelagem import Estado, Grafo, funcao_sucessora

def print_caminho(caminho, estado_inicial, custo_total, tempo, nos_expandidos):
    estado_atual = estado_inicial
    print(f"{0}: Estado inicial: {estado_atual}")
    for i, passo in enumerate(caminho):
        print(f"{i+1}: Passo: {passo.grupo_viajante} levam a tocha para o {'inicio' if passo.estado_destino.tocha_inicio else 'final'} (custo: {passo.custo})")
        estado_atual = passo.estado_destino
    print(f"Estado final: {estado_atual}")
    print(f"Custo total: {custo_total}, Tempo: {tempo:.6f}s, Nós expandidos: {nos_expandidos}")

def plot_metricas(resultados_algoritmos,colormap):
    algoritmos = list(resultados_algoritmos.keys())
    custo_total = [resultados_algoritmos[a][1] for a in algoritmos]
    tempo = [resultados_algoritmos[a][2] for a in algoritmos]
    nos_expandidos = [resultados_algoritmos[a][3] for a in algoritmos]

    colormap = colormaps[colormap]
    bar_colors = [colormap(i / len(algoritmos)) for i in range(len(algoritmos))]
    

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))

    axs[0].barh(algoritmos, custo_total, color=bar_colors)
    axs[0].set_title("Custo Total")
    axs[0].set_xlabel("Custo")

    axs[1].barh(algoritmos, tempo, color=bar_colors)
    axs[1].set_title("Tempo (s)")
    axs[1].set_xlabel("Segundos")

    axs[2].barh(algoritmos, nos_expandidos, color=bar_colors)
    axs[2].set_title("Nós Expandidos")
    axs[2].set_xlabel("Contagem")

    plt.tight_layout()
    plt.show()

def caminho_para_grafo(estado_inicial: Estado, caminho: list, nome_algoritmo: str = "algoritmo", descricao : str = ""):
    g = Grafo()

    for passo in caminho:
        g.adicionar_aresta(passo.estado_origem, passo.estado_destino, passo.custo)

    g.show(titulo=nome_algoritmo,descricao=descricao)



# Testes Gustavo:
def gerar_todos_estados():
    estados = []
    for bits in range(32):
        # extrair bits individuais
        A = bool(bits & 16)
        B = bool(bits & 8)
        C = bool(bits & 4)
        D = bool(bits & 2)
        T = bool(bits & 1)
        grupo_inicio = {p for p, lado in zip("ABCD", [A,B,C,D]) if not lado}
        tocha_inicio = not T
        estados.append(Estado(grupo_inicio, tocha_inicio))
    return estados

def construir_grafo_completo():
    G = nx.DiGraph()
    estados = gerar_todos_estados()
    for e in estados:
        for passo in funcao_sucessora(e):
            G.add_edge(str(e), str(passo.estado_destino), weight=passo.custo)
    return G

def plotar_grafo_completo_com_caminho(G, caminho_otimo):
    caminho_edges = set(
        (str(passo.estado_origem), str(passo.estado_destino)) for passo in caminho_otimo
    )
    pos = nx.spring_layout(G, seed=42, k=1.2)
    plt.figure(figsize=(18, 12))

    # todas as arestas em cinza
    nx.draw_networkx_edges(G, pos, edge_color="lightgray", width=1)

    # arestas do caminho ótimo em vermelho
    nx.draw_networkx_edges(
        G, pos,
        edgelist=caminho_edges,
        edge_color="red",
        width=2.5
    )

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color="lightblue")
    nx.draw_networkx_labels(G, pos, font_size=8)
    plt.title("Grafo completo (2^5 estados) com caminho ótimo em vermelho", fontsize=16)
    plt.show()