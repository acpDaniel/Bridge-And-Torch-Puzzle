import matplotlib.pyplot as plt
from matplotlib import colormaps

def print_caminho(algoritmo):
    """
    Exibe o caminho e as métricas do algoritmo em formato legível.
    """
    print(f"\n{'='*80}")
    print(f"🧩 {algoritmo.nome}")
    print(f"{'='*80}")

    estado_atual = algoritmo.dados.estado_inicial
    print(f"0: Estado inicial: {estado_atual}")

    for i, passo in enumerate(algoritmo.caminho, start=1):
        direcao = "início" if passo.estado_destino.tocha_inicio else "final"
        print(f"{i}: {passo.grupo_viajante} levam a tocha para o {direcao} (custo: {passo.custo})")
        estado_atual = passo.estado_destino

    print(f"Estado final: {estado_atual}")
    print(f"\n📊 Custo total: {algoritmo.custo_total}")
    print(f"⏱️ Tempo de execução: {algoritmo.tempo_exec:.6f}s")
    print(f"🌐 Nós expandidos: {algoritmo.nos_expandidos}")
    print(f"📍 Visitados: {len(algoritmo.visitados)}")
    print(f"{'='*80}\n")

def plot_metricas(algoritmos, colormap='Set3'):
    """
    Plota métricas comparativas (custo, tempo e nós expandidos) entre algoritmos.
    Mesma estrutura da função original, mas adaptada para receber objetos de algoritmo.
    """
    nomes = [a.nome for a in algoritmos]
    custo_total = [a.custo_total for a in algoritmos]
    tempo = [a.tempo_exec * 1000 for a in algoritmos]  # → ms
    nos_expandidos = [a.nos_expandidos for a in algoritmos]

    cmap = colormaps[colormap]
    bar_colors = [cmap(i / len(algoritmos)) for i in range(len(algoritmos))]

    fig, axs = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle("Métricas comparativas entre algoritmos")

    axs[0].barh(nomes, custo_total, color=bar_colors)
    axs[0].set_title("Custo Total")
    axs[0].set_xlabel("Custo")

    axs[1].barh(nomes, tempo, color=bar_colors)
    axs[1].set_title("Tempo (ms)")
    axs[1].set_xlabel("Milissegundos")

    axs[2].barh(nomes, nos_expandidos, color=bar_colors)
    axs[2].set_title("Nós Expandidos")
    axs[2].set_xlabel("Contagem")

    plt.tight_layout()
    plt.show()

