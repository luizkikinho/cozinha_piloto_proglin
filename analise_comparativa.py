import pandas as pd
from logica import subida_encosta, subida_encosta_tentativas, tempera_simulada
from avalia_sucessor import avalia_rota

def calcula_ganho(custo_inicial, custo_final):
    if custo_inicial == 0: return "0.00%"
    ganho = ((custo_inicial - custo_final) / custo_inicial) * 100
    return f"{ganho:.2f}%"

def executar_analise(rota_base, matriz, n):
    c_ini = avalia_rota(rota_base, matriz)

    ## Aviso: 'rota_inutil' significa que é temporário, apenas para análise
    
    # Subida de Encosta
    rota_inutil, c_se = subida_encosta(rota_base, matriz)

    # Subida de Encosta com Tentativa
    rota_inutil, c_set1 = subida_encosta_tentativas(rota_base, matriz, 2 * n)
    rota_inutil, c_set2 = subida_encosta_tentativas(rota_base, matriz, n)
    rota_inutil, c_set3 = subida_encosta_tentativas(rota_base, matriz, max(1, n // 2))

    # Têmpera Simulada
    rota_inutil, c_te1 = tempera_simulada(rota_base, matriz, 100, 0.1, 0.8)
    rota_inutil, c_te2 = tempera_simulada(rota_base, matriz, 200, 0.1, 0.8)
    rota_inutil, c_te3 = tempera_simulada(rota_base, matriz, 500, 0.1, 0.8)
    rota_inutil, c_te4 = tempera_simulada(rota_base, matriz, 200, 0.1, 0.9)
    rota_inutil, c_te5 = tempera_simulada(rota_base, matriz, 500, 0.1, 0.9)
    rota_inutil, c_te6 = tempera_simulada(rota_base, matriz, 200, 0.01, 0.9)
    rota_inutil, c_te7 = tempera_simulada(rota_base, matriz, 500, 0.01, 0.9)

    linhas_da_tabela = [
        ["SE",  "---",                    calcula_ganho(c_ini, c_se)],
        
        ["SET", "TMAX = 2*N",     calcula_ganho(c_ini, c_set1)],
        ["SET", "TMAX = N",     calcula_ganho(c_ini, c_set2)],
        ["SET", "TMAX = N/2",   calcula_ganho(c_ini, c_set3)],
        
        ["TE",  "TI=100; TF=0.1; FR=0.8", calcula_ganho(c_ini, c_te1)],
        ["TE",  "TI=200; TF=0.1; FR=0.8", calcula_ganho(c_ini, c_te2)],
        ["TE",  "TI=500; TF=0.1; FR=0.8", calcula_ganho(c_ini, c_te3)],
        ["TE",  "TI=200; TF=0.1; FR=0.9", calcula_ganho(c_ini, c_te4)],
        ["TE",  "TI=500; TF=0.1; FR=0.9", calcula_ganho(c_ini, c_te5)],
        ["TE",  "TI=200; TF=0.01; FR=0.9",calcula_ganho(c_ini, c_te6)],
        ["TE",  "TI=500; TF=0.01; FR=0.9",calcula_ganho(c_ini, c_te7)]
    ]

    df_tabela = pd.DataFrame(linhas_da_tabela, columns=["Método", "Observação", "Ganho"])

    return df_tabela