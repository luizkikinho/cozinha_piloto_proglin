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

    return soma / quantidade


def executar_analise(rota_base, matriz, n):
    c_ini = avalia_rota(rota_base, matriz)

    # Vetor que guarda o ganho dos 11 testes
    ganhos = []

    # =====================================================
    # 1. Subida de Encosta
    # =====================================================
    rota_inutil, c_se = subida_encosta(rota_base, matriz)
    g_se = calcula_ganho(c_ini, c_se)
    ganhos.append(g_se)

    # =====================================================
    # 2. SET - TMAX=N; TMAX = 2*N
    # =====================================================
    rota_inutil, c_set1 = subida_encosta_tentativas(
        rota_base,
        matriz,
        2 * n
    )
    g_set1 = calcula_ganho(c_ini, c_set1)
    ganhos.append(g_set1)

    # =====================================================
    # 3. SET - TMAX=N/2; TMAX = N
    # =====================================================
    rota_inutil, c_set2 = subida_encosta_tentativas(
        rota_base,
        matriz,
        n
    )
    g_set2 = calcula_ganho(c_ini, c_set2)
    ganhos.append(g_set2)

    # =====================================================
    # 4. SET - TMAX=N/4; TMAX = N/2
    # =====================================================
    rota_inutil, c_set3 = subida_encosta_tentativas(
        rota_base,
        matriz,
        max(1, int(n / 4))
    )
    g_set3 = calcula_ganho(c_ini, c_set3)
    ganhos.append(g_set3)

    # =====================================================
    # 5. TE - TI=100; TF=0.1; FR=0.8
    # =====================================================
    rota_inutil, c_te1 = tempera_simulada(
        rota_base,
        matriz,
        100,
        0.1,
        0.8
    )
    g_te1 = calcula_ganho(c_ini, c_te1)
    ganhos.append(g_te1)

    # =====================================================
    # 6. TE - TI=200; TF=0.1; FR=0.8
    # =====================================================
    rota_inutil, c_te2 = tempera_simulada(
        rota_base,
        matriz,
        200,
        0.1,
        0.8
    )
    g_te2 = calcula_ganho(c_ini, c_te2)
    ganhos.append(g_te2)

    # =====================================================
    # 7. TE - TI=500; TF=0.1; FR=0.8
    # =====================================================
    rota_inutil, c_te3 = tempera_simulada(
        rota_base,
        matriz,
        500,
        0.1,
        0.8
    )
    g_te3 = calcula_ganho(c_ini, c_te3)
    ganhos.append(g_te3)

    # =====================================================
    # 8. TE - TI=200; TF=0.1; FR=0.9
    # =====================================================
    rota_inutil, c_te4 = tempera_simulada(
        rota_base,
        matriz,
        200,
        0.1,
        0.9
    )
    g_te4 = calcula_ganho(c_ini, c_te4)
    ganhos.append(g_te4)

    # =====================================================
    # 9. TE - TI=500; TF=0.1; FR=0.9
    # =====================================================
    rota_inutil, c_te5 = tempera_simulada(
        rota_base,
        matriz,
        500,
        0.1,
        0.9
    )
    g_te5 = calcula_ganho(c_ini, c_te5)
    ganhos.append(g_te5)

    # =====================================================
    # 10. TE - TI=200; TF=0.01; FR=0.9
    # =====================================================
    rota_inutil, c_te6 = tempera_simulada(
        rota_base,
        matriz,
        200,
        0.01,
        0.9
    )
    g_te6 = calcula_ganho(c_ini, c_te6)
    ganhos.append(g_te6)

    # =====================================================
    # 11. TE - TI=500; TF=0.01; FR=0.9
    # =====================================================
    rota_inutil, c_te7 = tempera_simulada(
        rota_base,
        matriz,
        500,
        0.01,
        0.9
    )
    g_te7 = calcula_ganho(c_ini, c_te7)
    ganhos.append(g_te7)

    # =====================================================
    # Ganho médio geral
    # =====================================================
    ganho_medio_geral = calcula_media(ganhos)

    linhas_da_tabela = [
        ["SE",  "---", f"{g_se:.2f}%"],

        ["SET", "TMAX=N; TMAX = 2*N", f"{g_set1:.2f}%"],
        ["SET", "TMAX=N/2; TMAX = N", f"{g_set2:.2f}%"],
        ["SET", "TMAX=N/4; TMAX = N/2", f"{g_set3:.2f}%"],

        ["TE", "TI=100; TF=0.1; FR=0.8", f"{g_te1:.2f}%"],
        ["TE", "TI=200; TF=0.1; FR=0.8", f"{g_te2:.2f}%"],
        ["TE", "TI=500; TF=0.1; FR=0.8", f"{g_te3:.2f}%"],
        ["TE", "TI=200; TF=0.1; FR=0.9", f"{g_te4:.2f}%"],
        ["TE", "TI=500; TF=0.1; FR=0.9", f"{g_te5:.2f}%"],
        ["TE", "TI=200; TF=0.01; FR=0.9", f"{g_te6:.2f}%"],
        ["TE", "TI=500; TF=0.01; FR=0.9", f"{g_te7:.2f}%"],

        ["MÉDIA", "Ganho médio geral dos 11 testes", f"{ganho_medio_geral:.2f}%"]
    ]

    df_tabela = pd.DataFrame(
        linhas_da_tabela,
        columns=["Método", "Observação", "Ganho"]
    )

    return df_tabela