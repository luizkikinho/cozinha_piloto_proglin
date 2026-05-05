import random
import numpy as np

def obter_problema_fixo():
    escolas = [
        "Cozinha Piloto",
        "EMEF Dr. Evangelista Rodrigues - Centro",
        "EMEF Profª Regina Pompéia Pinto - São João",
        "EMEIEF Prof. Otton Fernandes Barbosa - Jd. Trabalhista",
        "EMEIEF Maria Zélia Freitas Lorena - Embauzinho",
        "EMEF Prof. Cleston Mello Paiva - Pitéu",
        "EMEF Profª Domingos de Paula Silva - Quilombo",
        "EMEFEP Prof. Joaquim Monteiro da Silva - Vila Carmem",
        "EMEIEF Yvone Cipolli Ribeiro - Jardim Europa"
    ]

    matriz = np.array([
        [0.0, 0.8, 2.4, 3.1, 6.8, 4.5, 5.2, 2.0, 2.7],
        [0.8, 0.0, 2.0, 2.8, 6.5, 4.1, 4.9, 1.6, 2.3],
        [2.4, 2.0, 0.0, 2.2, 7.4, 3.8, 5.9, 1.8, 1.5],
        [3.1, 2.8, 2.2, 0.0, 8.0, 5.1, 6.5, 3.4, 2.0],
        [6.8, 6.5, 7.4, 8.0, 0.0, 9.2, 4.3, 6.9, 7.8],
        [4.5, 4.1, 3.8, 5.1, 9.2, 0.0, 7.1, 4.0, 3.6],
        [5.2, 4.9, 5.9, 6.5, 4.3, 7.1, 0.0, 5.4, 6.2],
        [2.0, 1.6, 1.8, 3.4, 6.9, 4.0, 5.4, 0.0, 2.6],
        [2.7, 2.3, 1.5, 2.0, 7.8, 3.6, 6.2, 2.6, 0.0]
    ])

    return escolas, matriz

def gerar_problema_aleatorio(tamanho):
    escolas = [f"Escola {i}" for i in range(1, tamanho)]
    escolas.insert(0, "Cozinha Piloto") # Garante que o índice 0 é a Cozinha Piloto
    
    matriz = np.random.randint(1, 20, size=(tamanho, tamanho))
    matriz = (matriz + matriz.T) // 2 
    np.fill_diagonal(matriz, 0) 
    
    return escolas, matriz

def gerar_solucao_inicial(qtd_escolas):
    rota_intermediaria = list(range(1, qtd_escolas))
    random.shuffle(rota_intermediaria)
    solucao = [0] + rota_intermediaria + [0]
    return solucao