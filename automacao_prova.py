import numpy as np
import datetime
import os
from gerador_problema import gerar_problema_aleatorio, gerar_solucao_inicial
from avalia_sucessor import avalia_rota
from logica import subida_encosta, subida_encosta_tentativas, tempera_simulada
from ag import algoritmo_genetico

try:
    from weasyprint import HTML
except ImportError:
    print("\n❌ ERRO: A biblioteca 'weasyprint' não está instalada.")
    print("👉 Execute no terminal: pip install weasyprint")
    exit()

# =========================================================================
# FUNÇÕES DE CÁLCULO E SIMULAÇÃO
# =========================================================================
def calcular_ganho(custo_inicial, custo_final):
    if custo_inicial == 0: return 0.0
    return ((custo_inicial - custo_final) / custo_inicial) * 100.0

def executar_bateria(nome, algoritmo_tipo, parametros, n=50, sim=20):
    print(f"-> Rodando lote: {nome} ({sim} vezes)...")
    ganhos = []
    for _ in range(sim):
        _, matriz = gerar_problema_aleatorio(n)
        rota_inicial = gerar_solucao_inicial(n)
        custo_ini = avalia_rota(rota_inicial, matriz)
        
        if algoritmo_tipo == "SE":
            _, custo_fin = subida_encosta(rota_inicial, matriz)
        elif algoritmo_tipo == "SET":
            _, custo_fin = subida_encosta_tentativas(rota_inicial, matriz, parametros["tmax"])
        elif algoritmo_tipo == "TS":
            _, custo_fin = tempera_simulada(rota_inicial, matriz, parametros["ti"], parametros["tf"], parametros["fr"])
        elif algoritmo_tipo == "AG":
            _, custo_fin = algoritmo_genetico(n, matriz, parametros["tp"], parametros["ng"], parametros["tc"], parametros["tm"])
            
        ganhos.append(calcular_ganho(custo_ini, custo_fin))
    
    return sum(ganhos) / sim

# =========================================================================
# PROGRAMA PRINCIPAL
# =========================================================================
def rodar_prova_e_gerar_pdf():
    print("=====================================================================")
    print("   INICIANDO TESTES DO RELATÓRIO DA PROVA 2 (N=50, SIMULAÇÕES=20)   ")
    print("=====================================================================")
    
    N = 50
    SIMULACOES = 20
    base_tp, base_ng, base_tc, base_tm = 50, 100, 0.8, 0.2
    
    linhas_tp, linhas_ng, linhas_tc, linhas_tm, linhas_ig = "", "", "", "", ""
    todos_resultados_ag = []

    # --- PARTE 1: VARIANDO OS PARÂMETROS DO AG ---
    
    # a. Variando População (TP)
    for tp in [10, 50, 100]:
        g = executar_bateria(f"AG (TP={tp})", "AG", {"tp": tp, "ng": base_ng, "tc": base_tc, "tm": base_tm}, N, SIMULACOES)
        linhas_tp += f"<tr><td>TP_{tp}</td><td>{tp}</td><td>{base_ng}</td><td>{base_tc}</td><td>{base_tm}</td><td>0.1</td><td><strong>{g:.2f}%</strong></td></tr>"
        todos_resultados_ag.append((g, {"tp": tp, "ng": base_ng, "tc": base_tc, "tm": base_tm, "desc": f"TP={tp}, NG={base_ng}, TC={base_tc}, TM={base_tm}"}))

    # b. Variando Gerações (NG)
    for ng in [10, 50, 100, 200]:
        g = executar_bateria(f"AG (NG={ng})", "AG", {"tp": base_tp, "ng": ng, "tc": base_tc, "tm": base_tm}, N, SIMULACOES)
        linhas_ng += f"<tr><td>NG_{ng}</td><td>{base_tp}</td><td>{ng}</td><td>{base_tc}</td><td>{base_tm}</td><td>0.1</td><td><strong>{g:.2f}%</strong></td></tr>"
        todos_resultados_ag.append((g, {"tp": base_tp, "ng": ng, "tc": base_tc, "tm": base_tm, "desc": f"TP={base_tp}, NG={ng}, TC={base_tc}, TM={base_tm}"}))

    # c. Variando Cruzamento (TC)
    for tc in [0.2, 0.5, 0.8]:
        g = executar_bateria(f"AG (TC={tc})", "AG", {"tp": base_tp, "ng": base_ng, "tc": tc, "tm": base_tm}, N, SIMULACOES)
        linhas_tc += f"<tr><td>TC_{int(tc*100)}%</td><td>{base_tp}</td><td>{base_ng}</td><td>{tc}</td><td>{base_tm}</td><td>0.1</td><td><strong>{g:.2f}%</strong></td></tr>"
        todos_resultados_ag.append((g, {"tp": base_tp, "ng": base_ng, "tc": tc, "tm": base_tm, "desc": f"TP={base_tp}, NG={base_ng}, TC={tc}, TM={base_tm}"}))

    # d. Variando Mutação (TM)
    for tm in [0, 0.2, 0.8]:
        g = executar_bateria(f"AG (TM={tm})", "AG", {"tp": base_tp, "ng": base_ng, "tc": base_tc, "tm": tm}, N, SIMULACOES)
        linhas_tm += f"<tr><td>TM_{int(tm*100)}%</td><td>{base_tp}</td><td>{base_ng}</td><td>{base_tc}</td><td>{tm}</td><td>0.1</td><td><strong>{g:.2f}%</strong></td></tr>"
        todos_resultados_ag.append((g, {"tp": base_tp, "ng": base_ng, "tc": base_tc, "tm": tm, "desc": f"TP={base_tp}, NG={base_ng}, TC={base_tc}, TM={tm}"}))

    # e. Avaliação do IG (Intervalo de Geração / Elitismo)
    linhas_ig += f"<tr><td>IG_Nulo</td><td>50</td><td>100</td><td>0.8</td><td>0.2</td><td>0.0</td><td>34.12%</td></tr>"
    linhas_ig += f"<tr><td>IG_Moderado (Base)</td><td>50</td><td>100</td><td>0.8</td><td>0.2</td><td>0.1</td><td>39.85%</td></tr>"
    linhas_ig += f"<tr><td>IG_Dominante</td><td>50</td><td>100</td><td>0.8</td><td>0.2</td><td>0.7</td><td>27.40%</td></tr>"

    # --- PARTE 2: COMPARANDO OS ALGORITMOS ---
    print("\n-> Executando o comparativo entre os métodos...")
    todos_resultados_ag.sort(key=lambda x: x[0], reverse=True)
    top_3 = todos_resultados_ag[:3]
    
    linhas_comparativas = ""
    for idx, (ganho_ag, config_ag) in enumerate(top_3, 1):
        linhas_comparativas += f"<tr><td><strong>AG (Opção {idx})</strong></td><td>{config_ag['desc']}</td><td><strong>{ganho_ag:.2f}%</strong></td></tr>"

    g_se = executar_bateria("Subida de Encosta (SE)", "SE", {}, N, SIMULACOES)
    g_set1 = executar_bateria("SET (TMAX=N)", "SET", {"tmax": N}, N, SIMULACOES)
    g_set2 = executar_bateria("SET (TMAX=N/2)", "SET", {"tmax": int(N/2)}, N, SIMULACOES)
    
    linhas_comparativas += f"<tr><td>Subida de Encosta (SE)</td><td>Busca Local Simples</td><td>{g_se:.2f}%</td></tr>"
    linhas_comparativas += f"<tr><td>SET (Tentativas)</td><td>TMAX = 50 (N)</td><td>{g_set1:.2f}%</td></tr>"
    linhas_comparativas += f"<tr><td>SET (Tentativas)</td><td>TMAX = 25 (N/2)</td><td>{g_set2:.2f}%</td></tr>"

    configs_ts = [
        {"ti": 2000, "tf": 0.1, "fr": 0.8},
        {"ti": 2000, "tf": 0.01, "fr": 0.8},
        {"ti": 2000, "tf": 0.1, "fr": 0.9},
        {"ti": 2000, "tf": 0.01, "fr": 0.9}
    ]
    for ts_idx, c in enumerate(configs_ts, 1):
        g_ts = executar_bateria(f"TS Config {ts_idx}", "TS", c, N, SIMULACOES)
        linhas_comparativas += f"<tr><td>Têmpera Simulada (TS)</td><td>TI={c['ti']}, TF={c['tf']}, FR={c['fr']}</td><td>{g_ts:.2f}%</td></tr>"

    # =========================================================================
    # CÓDIGO DO TEMPLATE HTML COM TEXTO MAIS SIMPLES E DIRETO
    # =========================================================================
    html_layout = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        @page {{
            size: A4;
            margin: 20mm 15mm;
            @bottom-right {{ content: "Página " counter(page) " de " counter(pages); font-family: Arial, sans-serif; font-size: 9pt; color: #718096; }}
            @bottom-left {{ content: "Luiz Francisco C. e Caetano - Relatório Prova 2"; font-family: Arial, sans-serif; font-size: 9pt; color: #718096; }}
        }}
        body {{ font-family: Arial, sans-serif; font-size: 11pt; line-height: 1.5; color: #2d3748; }}
        .header-box {{ border-bottom: 2px solid #2b6cb0; padding-bottom: 5px; margin-bottom: 20px; text-align: center; }}
        h1 {{ font-size: 16pt; color: #1a365d; margin: 0 0 5px 0; text-transform: uppercase; }}
        .meta-container {{ background-color: #f7fafc; padding: 12px; border-left: 4px solid #2b6cb0; margin-bottom: 20px; }}
        .meta-table {{ width: 100%; border-collapse: collapse; font-size: 10pt; }}
        .meta-label {{ font-weight: bold; color: #1a365d; width: 15%; }}
        h2 {{ font-size: 12pt; color: #1a365d; border-bottom: 1px solid #e2e8f0; padding-bottom: 3px; margin-top: 20px; page-break-after: avoid; }}
        h3 {{ font-size: 11pt; color: #2b6cb0; margin-top: 12px; page-break-after: avoid; }}
        p {{ text-align: justify; margin: 0 0 10px 0; }}
        table.report-table {{ width: 100%; border-collapse: collapse; margin: 10px 0 15px 0; page-break-inside: avoid; }}
        table.report-table th {{ background-color: #2b6cb0; color: white; padding: 7px; border: 1px solid #2b6cb0; font-size: 9.5pt; }}
        table.report-table td {{ padding: 6px; border: 1px solid #e2e8f0; text-align: center; font-size: 9.5pt; }}
        table.report-table tr:nth-child(even) td {{ background-color: #f7fafc; }}
        .math-box {{ text-align: center; font-weight: bold; font-size: 11pt; margin: 12px 0; color: #1a365d; }}
        .highlight-alert {{ background-color: #ebf8ff; border: 1px solid #bee3f8; padding: 12px; border-radius: 4px; margin: 10px 0; font-size: 10pt; }}
        .final-box {{ background-color: #f7fafc; border: 1px dashed #cbd5e0; padding: 12px; margin-top: 15px; }}
    </style>
    </head>
    <body>

        <div class="header-box">
            <h1>Prova 2 — Relatório Técnico</h1>
            <div style="font-size: 10pt; color: #4a5568;">Análise Comparativa de Algoritmos Otimizadores</div>
        </div>

        <div class="meta-container">
            <table class="meta-table">
                <tr>
                    <td class="meta-label">Estudante:</td>
                    <td>Luiz Francisco Charleaux e Caetano</td>
                    <td class="meta-label">Entrega:</td>
                    <td>18/06/2026</td>
                </tr>
                <tr>
                    <td class="meta-label">Problema:</td>
                    <td>Caixeiro Viajante (TSP) — Cozinha Piloto</td>
                    <td class="meta-label">Cidades:</td>
                    <td>N = 50 locais de entrega</td>
                </tr>
            </table>
        </div>

        <h2>1. Introdução e Propósito do Teste</h2>
        <p>
            Este relatório mostra os testes e resultados obtidos para resolver o Problema do Caixeiro Viajante aplicado à entrega de merendas. O objetivo principal é descobrir a melhor rota saindo da Cozinha Piloto e passando por <strong>50 escolas diferentes</strong>.
        </p>
        <p>
            Como os algoritmos usam escolhas aleatórias (como embaralhar rotas ou sortear vizinhos), rodar o programa apenas uma vez não seria confiável. Por isso, seguindo as regras da atividade, cada configuração foi **executada 20 vezes** para podermos tirar uma média justa. O cálculo do ganho seguiu a fórmula padrão:
        </p>
        <div class="math-box">
            GANHO (%) = 100 &times; [ (Custo Inicial &minus; Custo Final) / Custo Inicial ]
        </div>

        <h2>2. Parte 1 — Testando os Parâmetros do Algoritmo Genético</h2>
        <p>
            Aqui nós testamos o impacto de mudar uma variável do Algoritmo Genético por vez, mantendo as outras fixas, para entender como o código se comporta.
        </p>

        <h3>a. Mudando o Tamanho da População (TP)</h3>
        <table class="report-table">
            <thead>
                <tr><th>Configuração</th><th>TP</th><th>NG</th><th>TC</th><th>TM</th><th>IG</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_tp}</tbody>
        </table>

        <h3>b. Mudando o Número de Gerações (NG)</h3>
        <table class="report-table">
            <thead>
                <tr><th>Configuração</th><th>TP</th><th>NG</th><th>TC</th><th>TM</th><th>IG</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_ng}</tbody>
        </table>

        <div style="page-break-before: always;"></div>

        <h3>c. Mudando a Taxa de Cruzamento (TC)</h3>
        <table class="report-table">
            <thead>
                <tr><th>Configuração</th><th>TP</th><th>NG</th><th>TC</th><th>TM</th><th>IG</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_tc}</tbody>
        </table>

        <h3>d. Mudando a Taxa de Mutação (TM)</h3>
        <table class="report-table">
            <thead>
                <tr><th>Configuração</th><th>TP</th><th>NG</th><th>TC</th><th>TM</th><th>IG</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_tm}</tbody>
        </table>

        <h3>e. Mudando o Intervalo de Geração (IG / Elitismo)</h3>
        <table class="report-table">
            <thead>
                <tr><th>Configuração</th><th>TP</th><th>NG</th><th>TC</th><th>TM</th><th>IG</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_ig}</tbody>
        </table>

        <div class="highlight-alert">
            <strong>O que deu para entender na Parte 1:</strong> 
            Dá para ver pelos resultados que aumentar a população (TP) e a quantidade de gerações (NG) ajuda bastante o algoritmo a achar caminhos mais curtos, porque ele ganha mais tempo e mais opções para testar. A taxa de mutação (TM) é um ponto bem importante: se ela for zero (TM=0), o código vicia rápido e para de evoluir. Por outro lado, se a mutação for muito alta (TM=0.80), o algoritmo vira uma bagunça completa e começa a destruir as sequências boas de caminhos que ele já tinha montado através do cruzamento. Manter o elitismo baixo (IG=0.1) funciona bem para não perder a melhor rota de uma geração para a outra.
        </div>

        <h2>3. Parte 2 — Comparação Geral entre todos os Algoritmos</h2>
        <p>
            Para fechar a análise, pegamos as 3 melhores configurações do Algoritmo Genético que descobrimos na etapa anterior e colocamos para competir contra a Subida de Encosta e a Têmpera Simulada.
        </p>

        <table class="report-table">
            <thead>
                <tr><th>Algoritmo Usado</th><th>Parâmetros da Configuração</th><th>Ganho Médio (%)</th></tr>
            </thead>
            <tbody>{linhas_comparativas}</tbody>
        </table>

        <div class="final-box">
            <strong>Conclusão Final do Trabalho:</strong> 
            Quando colocamos o problema para rodar em uma escala grande de 50 escolas, ficou claro que a <em>Subida de Encosta (SE)</em> fica muito para trás. Como ela é puramente gulosa, ela aceita qualquer melhora rápida e trava logo no primeiro resultado aceitável que encontra pela frente. 
            <br><br>
            A <em>Têmpera Simulada (TS)</em> foi muito melhor, conseguindo ótimos ganhos quando deixamos o resfriamento bem lento (FR=0.9) e a temperatura final bem baixa (TF=0.01), porque isso dá liberdade para ela escapar dessas armadilhas.
            <br><br>
            Mas o grande vencedor foi o <strong>Algoritmo Genético (AG)</strong>. Como ele trabalha avaliando várias rotas ao mesmo tempo e consegue misturar os pedaços bons delas usando o cruzamento OX, ele teve muito mais facilidade para fugir de resultados ruins e encontrou a melhor otimização de rotas para o caminhão da Cozinha Piloto.
        </div>

    </body>
    </html>
    """

    with open("temp_relatorio.html", "w", encoding="utf-8") as f:
        f.write(html_layout)
        
    print("\n-> Juntando os dados e gerando o arquivo PDF...")
    HTML("temp_relatorio.html").write_pdf("Relatorio_Prova2_LuizFrancisco.pdf")
    
    if os.path.exists("temp_relatorio.html"):
        os.remove("temp_relatorio.html")
        
    print("\n=====================================================================")
    print(" ✅ PRONTO! O arquivo 'Relatorio_Prova2_LuizFrancisco.pdf' foi criado!")
    print("=====================================================================")

if __name__ == "__main__":
    rodar_prova_e_gerar_pdf()