import numpy as np
import random
from avalia_sucessor import avalia_rota

## Fitness
def aptidao(pop, matriz):
    tp = len(pop)
    fit = np.zeros(tp, float)

    for i in range(tp):
        custo = avalia_rota(pop[i], matriz)
        if custo == 0:
            fit[i] = 100000
        else:
            fit[i] = 1.0 / custo
    
    soma = sum(fit)
    if soma > 0:
        fit = fit / soma
    
    return fit

## Roleta
def roleta (fit, tp):
    ale = random.uniform(0, 1)
    ind = 0
    soma = fit[ind]

    while soma < ale and ind < tp - 1:
        ind += 1
        soma += fit[ind]

    return ind

## Cruzamento de ordem (PCV)
def cruzamento_ox(pai1, pai2):
    tamanho = len(pai1)

    # Para proteger a restrição principal, que deve começar e terminar do ponto 0
    miolo_p1 = pai1[1:-1]
    miolo_p2 = pai2[1:-1]

    n = len(miolo_p1)

    corte1, corte2 = sorted(random.sample(range(n), 2))

    # Filho 1 recebe o trecho do Pai 1
    filho1_miolo = [-1] * n
    filho1_miolo[corte1:corte2] = miolo_p1[corte1:corte2]

    # Preenche o resto com trechos do Pai 2
    pos_f1 = corte2
    for gene in miolo_p2:
        if gene not in filho1_miolo:
            if pos_f1 == n:
                pos_f1 = 0
            filho1_miolo[pos_f1] = gene
            pos_f1 += 1
    
    # Remonta a rota com 0 nas pontas
    filho1 = [0] + filho1_miolo + [0]
    return filho1

## Mutação por troca de posição
def mutacao_swap(rota):
    pos1 = random.randint(1, len(rota) - 2)
    pos2 = random.randint(1, len(rota) - 2)

    rota[pos1], rota[pos2] = rota[pos2], rota[pos1]
    return rota

## Função principal
def algoritmo_genetico(escolas_qtd, matriz, tp, ng, tc, tm):
    
    # População Inicial
    pop = []
    for _ in range(tp):
        miolo = list(range(1, escolas_qtd))
        random.shuffle(miolo)
        rota = [0] + miolo + [0]
        pop.append(rota)
    
    melhor_rota_global = pop[0]
    melhor_custo_global = avalia_rota(pop[0], matriz)

    # Laço de gerações
    for geracao in range(ng):
        fit = aptidao(pop, matriz)
        nova_pop = []

        # Descendentes
        while len(nova_pop) < tp:
            idx_pai1 = roleta(fit, tp)
            idx_pai2 = roleta(fit, tp)
            pai1 = pop[idx_pai1]
            pai2 = pop[idx_pai2]

            if random.random() <= tc:
                filho = cruzamento_ox(pai1, pai2)
            else:
                filho = pai1.copy() # Se não houver cruzamento, será o mesmo que o pai

            # Mutação
            if random.random() <= tm:
                filho = mutacao_swap(filho)
            
            nova_pop.append(filho)
        
        pop = nova_pop

        for rota in pop:
            custo_atual = avalia_rota(rota, matriz)
            if custo_atual < melhor_custo_global:
                melhor_custo_global = custo_atual
                melhor_rota_global = rota.copy()
    
    return melhor_rota_global, melhor_custo_global