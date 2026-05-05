import math
import random
from avalia_sucessor import avalia_rota, sucessor

def subida_encosta(rota_inicial, matriz):
    atual = rota_inicial
    va = avalia_rota(atual, matriz)

    while True:
        novo, vn = sucessor(atual, va, matriz)
        if va > vn:
            atual = novo
            va = vn
        else:
            return atual, va


def subida_encosta_tentativas(rota_inicial, matriz, tmax):
    atual = rota_inicial
    va = avalia_rota(atual, matriz)
    
    t = 0
    
    while t < tmax:
        novo, vn = sucessor(atual, va, matriz)
        
        if vn < va:
            atual = novo
            va = vn
            t = 0
        else:
            t = t + 1    
    return atual, va

from avalia_sucessor import avalia_rota, sucessor

def tempera_simulada(rota_inicial, matriz, ti, tf, fr):
    atual = rota_inicial
    va = avalia_rota(atual, matriz)

    t = ti # Inicia com temperatura alta

    while t > tf:
        novo, vn = sucessor(atual, va, matriz)
        if vn < va:
            atual = novo
            va = vn
        else:
            d = vn - va
            aux = math.exp(-d/t)
            ale = random.random()
            if ale < aux:
                atual = novo
                va = vn
        
        t = t * fr

    return atual, va