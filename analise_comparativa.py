import pandas as pd

from logica import subida_encosta, subida_encosta_tentativas, tempera_simulada
from avalia_sucessor import avalia_rota


def calcula_ganho(custo_inicial, custo_final):
    if custo_inicial == 0:
        return 0.0

    ganho = ((custo_inicial - custo_final) / custo_inicial) * 100
    return ganho


def calcula_media(vetor_ganhos):
    if len(vetor_ganhos) == 0:
        return 0.0

    soma = sum(vetor_ganhos)
    quantidade = len(vetor_ganhos)

    media = soma / quantidade
    return media


def executar_analise(rota_base, matriz, n):
    c_ini = avalia_rota(rota_base, matriz)

    quantidade_iteracoes = 30

    # SE - Subida de Encosta
    ganhos_se = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = subida_encosta(rota_base, matriz)

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_se.append(ganho)

    media_se = calcula_media(ganhos_se)

    # SET 1 - TMAX=N; TMAX = 2*N
    ganhos_set1 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = subida_encosta_tentativas(
            rota_base,
            matriz,
            2 * n
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_set1.append(ganho)

    media_set1 = calcula_media(ganhos_set1)

    # SET 2 - TMAX=N/2; TMAX = N
    ganhos_set2 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = subida_encosta_tentativas(
            rota_base,
            matriz,
            n
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_set2.append(ganho)

    media_set2 = calcula_media(ganhos_set2)

    # SET 3 - TMAX=N/4; TMAX = N/2
    ganhos_set3 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = subida_encosta_tentativas(
            rota_base,
            matriz,
            max(1, int(n / 4))
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_set3.append(ganho)

    media_set3 = calcula_media(ganhos_set3)

    # TE 1 - TI=100; TF=0.1; FR=0.8
    ganhos_te1 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            100,
            0.1,
            0.8
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te1.append(ganho)

    media_te1 = calcula_media(ganhos_te1)

    # TE 2 - TI=200; TF=0.1; FR=0.8
    ganhos_te2 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            200,
            0.1,
            0.8
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te2.append(ganho)

    media_te2 = calcula_media(ganhos_te2)

    # TE 3 - TI=500; TF=0.1; FR=0.8
    ganhos_te3 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            500,
            0.1,
            0.8
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te3.append(ganho)

    media_te3 = calcula_media(ganhos_te3)

    # TE 4 - TI=200; TF=0.1; FR=0.9
    ganhos_te4 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            200,
            0.1,
            0.9
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te4.append(ganho)

    media_te4 = calcula_media(ganhos_te4)

    # TE 5 - TI=500; TF=0.1; FR=0.9
    ganhos_te5 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            500,
            0.1,
            0.9
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te5.append(ganho)

    media_te5 = calcula_media(ganhos_te5)

    # TE 6 - TI=200; TF=0.01; FR=0.9
    ganhos_te6 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            200,
            0.01,
            0.9
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te6.append(ganho)

    media_te6 = calcula_media(ganhos_te6)

    # TE 7 - TI=500; TF=0.01; FR=0.9
    ganhos_te7 = []

    for i in range(quantidade_iteracoes):
        rota_inutil, custo_final = tempera_simulada(
            rota_base,
            matriz,
            500,
            0.01,
            0.9
        )

        ganho = calcula_ganho(c_ini, custo_final)
        ganhos_te7.append(ganho)

    media_te7 = calcula_media(ganhos_te7)

    # Tabela final
    linhas_da_tabela = [
        ["SE", "---", f"{media_se:.2f}%"],

        ["SET", "TMAX=N; TMAX = 2*N", f"{media_set1:.2f}%"],
        ["SET", "TMAX=N/2; TMAX = N", f"{media_set2:.2f}%"],
        ["SET", "TMAX=N/4; TMAX = N/2", f"{media_set3:.2f}%"],

        ["TE", "TI=100; TF=0.1; FR=0.8", f"{media_te1:.2f}%"],
        ["TE", "TI=200; TF=0.1; FR=0.8", f"{media_te2:.2f}%"],
        ["TE", "TI=500; TF=0.1; FR=0.8", f"{media_te3:.2f}%"],
        ["TE", "TI=200; TF=0.1; FR=0.9", f"{media_te4:.2f}%"],
        ["TE", "TI=500; TF=0.1; FR=0.9", f"{media_te5:.2f}%"],
        ["TE", "TI=200; TF=0.01; FR=0.9", f"{media_te6:.2f}%"],
        ["TE", "TI=500; TF=0.01; FR=0.9", f"{media_te7:.2f}%"]
    ]

    df_tabela = pd.DataFrame(
        linhas_da_tabela,
        columns=["Método", "Observação", "Ganho Médio"]
    )

    return df_tabela