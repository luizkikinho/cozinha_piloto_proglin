import random
def avalia_rota(rota, matriz):
    # Função avalia, percorre a rota somando as distâncias consultadas na matriz
    custo_total = 0.0
    for i in range(len(rota) - 1):
        atual = rota[i]
        proximo = rota[i + 1]
        custo_total += matriz[atual][proximo]
    return custo_total


def sucessor(atual, va, matriz):
    # Método sucessor (Caixeiro Viajante)

    n = len(atual)
    
    # Sorteia a posição 'p' (pivô)
    p = random.randint(1, n - 2)

    flag = True
    melhor_rota = None
    vm = 0 # Valor do melhor

    for i in range(1, n - 1):
        if i != p:
            suc = atual.copy() # Cria uma cópia para segurança
            suc[i], suc[p] = suc[p], suc[i] # Faz a troca dos valores
            vs = avalia_rota(suc, matriz)
            if flag:
                melhor_rota = suc
                vm = vs
                flag = False
            
            else:
                if vs < vm:
                    melhor_rota = suc
                    vm = vs
                    
    return melhor_rota, vm
            