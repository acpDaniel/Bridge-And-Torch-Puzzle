import heapq
from time import time
from collections import deque
from modelagem import Estado, TEMPOS, funcao_sucessora

def bfs(estado_inicial : Estado, estado_objetivo : Estado):
    inicio = time()
    
    visitados = set()
    visitados.add(estado_inicial)
    
    fila = deque()
    fila.append((estado_inicial, [], 0))
    
    nos_expandidos = 0
    
    while fila:
        estado_atual, caminho, custo_atual = fila.popleft()
        nos_expandidos += 1
        
        for passo in funcao_sucessora(estado_atual):
            # se o sucessor é o estado final, terminamos
            if passo.estado_destino.grupo_inicio == estado_objetivo.grupo_inicio:
                fim = time()
                caminho_completo = caminho + [passo]
                return caminho_completo, custo_atual + passo.custo, fim - inicio, nos_expandidos

            if passo.estado_destino not in visitados:
                visitados.add(passo.estado_destino)
                novo_caminho = caminho + [passo]
                fila.append((passo.estado_destino, novo_caminho, custo_atual + passo.custo))
    
    fim = time()
    return None, None, fim - inicio, nos_expandidos

def dfs(estado_inicial: Estado, estado_objetivo: Estado, limite=10_000):
    inicio = time()
    
    visitados = set()
    pilha = [(estado_inicial, [], 0)]
    
    nos_expandidos = 0
    
    while pilha and nos_expandidos < limite:
        estado_atual, caminho, custo_atual = pilha.pop()
        
        if estado_atual in visitados:
            continue
        visitados.add(estado_atual)

        nos_expandidos += 1
        
        if estado_atual == estado_objetivo:
            fim = time()
            return caminho, custo_atual, fim - inicio, nos_expandidos

        for passo in funcao_sucessora(estado_atual):
            novo_caminho = caminho + [passo]
            pilha.append((passo.estado_destino, novo_caminho, custo_atual + passo.custo))
    
    fim = time()
    return None, None, fim - inicio, nos_expandidos

def custo_uniforme(estado_inicial: Estado, estado_objetivo: Estado):
    inicio = time()
    
    visitados = set()
    visitados.add(estado_inicial)
    
    heap = []
    # contador para desempatar (evitando que a comparação vá para Estado, que não tem comparação, por não ter custo associado à um estado individual.)
    contador = 0
    heapq.heappush(heap, (0, contador, estado_inicial, []))
    
    nos_expandidos = 0
    
    while heap:
        custo_atual, _, estado_atual, caminho = heapq.heappop(heap)
        nos_expandidos += 1
        
        for passo in funcao_sucessora(estado_atual):
            estado_sucessor = passo.estado_destino
            novo_custo = custo_atual + passo.custo
            
            # se o sucessor é o estado final, terminamos
            if estado_sucessor.grupo_inicio == estado_objetivo.grupo_inicio:
                fim = time()
                caminho_completo = caminho + [passo]
                return caminho_completo, novo_custo, fim - inicio, nos_expandidos
            
            if estado_sucessor not in visitados:
                visitados.add(estado_sucessor)
                novo_caminho = caminho + [passo]
                contador += 1  # incrementa o contador para desempate
                heapq.heappush(heap, (novo_custo, contador, estado_sucessor, novo_caminho))
    
    fim = time()
    return None, None, fim - inicio, nos_expandidos

def a_estrela(estado_inicial: Estado, estado_objetivo: Estado, funcao_heuristica):
    inicio = time()
    
    visitados = set()
    visitados.add(estado_inicial)
    
    heap = []
    contador = 0
    f0 = funcao_heuristica(estado_inicial)
    heapq.heappush(heap, (f0, contador, 0, estado_inicial, []))
    
    nos_expandidos = 0
    
    while heap:
        f_atual, _, g_atual, estado_atual, caminho = heapq.heappop(heap)
        nos_expandidos += 1
        
        for passo in funcao_sucessora(estado_atual):
            estado_sucessor = passo.estado_destino
            g_novo = g_atual + passo.custo
            f_novo = g_novo + funcao_heuristica(estado_sucessor)
            
            # se o sucessor é o estado final, terminamos
            if estado_sucessor.grupo_inicio == estado_objetivo.grupo_inicio:
                fim = time()
                caminho_completo = caminho + [passo]
                return caminho_completo, g_novo, fim - inicio, nos_expandidos
            
            if estado_sucessor not in visitados:
                visitados.add(estado_sucessor)
                novo_caminho = caminho + [passo]
                contador += 1
                heapq.heappush(heap, (f_novo, contador, g_novo, estado_sucessor, novo_caminho))
    
    fim = time()
    return None, None, fim - inicio, nos_expandidos