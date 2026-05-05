import streamlit as st
import pandas as pd

from logica import (
    subida_encosta,
    subida_encosta_tentativas,
    tempera_simulada
)

from gerador_problema import (
    obter_problema_fixo, 
    gerar_problema_aleatorio, 
    gerar_solucao_inicialimport streamlit as st
import pandas as pd

from logica import (
    subida_encosta,
    subida_encosta_tentativas,
    tempera_simulada
)

from gerador_problema import (
    obter_problema_fixo,
    gerar_problema_aleatorio,
    gerar_solucao_inicial
)

from avalia_sucessor import avalia_rota

from analise_comparativa import executar_analise


# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================

st.set_page_config(
    page_title="Cozinha Piloto | Otimização de Rotas",
    page_icon="🚚",
    layout="wide"
)


# =========================================================
# ESTILO VISUAL
# =========================================================

def carregar_estilos():
    st.markdown("""
    <style>
        /* ===============================
           BASE
        =============================== */

        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(56, 189, 248, 0.18), transparent 28%),
                radial-gradient(circle at 88% 20%, rgba(251, 191, 36, 0.10), transparent 24%),
                linear-gradient(135deg, #020617 0%, #0f172a 48%, #111827 100%);
            color: #f8fafc;
        }

        .block-container {
            max-width: 1320px;
            padding-top: 1.8rem;
            padding-bottom: 3rem;
        }

        h1, h2, h3 {
            color: #f8fafc !important;
            letter-spacing: -0.035em;
        }

        p, span, label, div {
            color: inherit;
        }

        hr {
            border-color: rgba(148, 163, 184, 0.18);
        }

        /* ===============================
           SIDEBAR
        =============================== */

        [data-testid="stSidebar"] {
            background:
                linear-gradient(180deg, #020617 0%, #0f172a 60%, #111827 100%);
            border-right: 1px solid rgba(148, 163, 184, 0.18);
        }

        [data-testid="stSidebar"] * {
            color: #f8fafc;
        }

        [data-testid="stSidebar"] [role="radiogroup"] label {
            background: rgba(15, 23, 42, 0.70);
            border: 1px solid rgba(148, 163, 184, 0.16);
            padding: 0.55rem 0.75rem;
            border-radius: 12px;
            margin-bottom: 0.35rem;
        }

        /* ===============================
           FORMULÁRIOS
        =============================== */

        .stSelectbox label,
        .stNumberInput label,
        .stRadio label {
            color: #f8fafc !important;
            font-weight: 750;
        }

        div[data-baseweb="select"] > div,
        div[data-baseweb="input"] {
            background-color: rgba(15, 23, 42, 0.96);
            border: 1px solid rgba(148, 163, 184, 0.34);
            color: #f8fafc;
            border-radius: 14px;
        }

        input {
            color: #f8fafc !important;
        }

        input:focus,
        textarea:focus,
        div[data-baseweb="select"] > div:focus-within {
            outline: 2px solid #38bdf8 !important;
            outline-offset: 2px;
        }

        /* ===============================
           BOTÕES
        =============================== */

        .stButton > button {
            width: 100%;
            border-radius: 14px;
            border: 1px solid rgba(125, 211, 252, 0.38);
            background:
                linear-gradient(135deg, #0284c7 0%, #2563eb 55%, #1d4ed8 100%);
            color: #ffffff;
            font-weight: 850;
            min-height: 3rem;
            box-shadow: 0 12px 28px rgba(37, 99, 235, 0.22);
            transition: all 0.18s ease;
        }

        .stButton > button:hover {
            transform: translateY(-2px);
            border-color: rgba(186, 230, 253, 0.8);
            box-shadow: 0 18px 34px rgba(37, 99, 235, 0.34);
            color: #ffffff;
        }

        .stButton > button:focus {
            outline: 3px solid #facc15 !important;
            outline-offset: 3px;
        }

        /* ===============================
           BLOCOS VISUAIS
        =============================== */

        .top-panel {
            display: grid;
            grid-template-columns: 1.45fr 0.85fr;
            gap: 1rem;
            margin-bottom: 1.25rem;
        }

        .mission-card {
            background:
                linear-gradient(135deg, rgba(8, 47, 73, 0.96), rgba(15, 23, 42, 0.95));
            border: 1px solid rgba(125, 211, 252, 0.25);
            border-radius: 28px;
            padding: 2rem;
            box-shadow: 0 24px 58px rgba(2, 6, 23, 0.46);
        }

        .mission-kicker {
            color: #7dd3fc;
            font-size: 0.82rem;
            text-transform: uppercase;
            letter-spacing: 0.16em;
            font-weight: 900;
            margin-bottom: 0.5rem;
        }

        .mission-title {
            font-size: 2.65rem;
            line-height: 1.02;
            font-weight: 950;
            color: #ffffff;
            letter-spacing: -0.06em;
            margin-bottom: 0.85rem;
        }

        .mission-text {
            color: #cbd5e1;
            line-height: 1.65;
            font-size: 1.02rem;
            max-width: 820px;
        }

        .identity-card {
            background:
                linear-gradient(180deg, rgba(30, 41, 59, 0.92), rgba(15, 23, 42, 0.92));
            border: 1px solid rgba(250, 204, 21, 0.22);
            border-radius: 28px;
            padding: 1.4rem;
            box-shadow: 0 24px 58px rgba(2, 6, 23, 0.36);
        }

        .identity-label {
            color: #fde68a;
            font-size: 0.78rem;
            text-transform: uppercase;
            letter-spacing: 0.14em;
            font-weight: 900;
            margin-bottom: 0.75rem;
        }

        .identity-row {
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 0.7rem;
            border-top: 1px solid rgba(148, 163, 184, 0.14);
            padding: 0.72rem 0;
            color: #e2e8f0;
            font-size: 0.95rem;
        }

        .identity-row strong {
            color: #f8fafc;
        }

        .workflow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 1.25rem 0 1.6rem 0;
        }

        .step-card {
            background: rgba(15, 23, 42, 0.82);
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 20px;
            padding: 1rem;
            min-height: 120px;
            box-shadow: 0 16px 36px rgba(2, 6, 23, 0.32);
        }

        .step-number {
            width: 2rem;
            height: 2rem;
            border-radius: 999px;
            background: rgba(56, 189, 248, 0.12);
            border: 1px solid rgba(125, 211, 252, 0.45);
            color: #7dd3fc;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 950;
            margin-bottom: 0.7rem;
        }

        .step-title {
            color: #f8fafc;
            font-weight: 900;
            margin-bottom: 0.25rem;
        }

        .step-desc {
            color: #94a3b8;
            font-size: 0.9rem;
            line-height: 1.45;
        }

        .operation-card {
            background:
                linear-gradient(180deg, rgba(15, 23, 42, 0.90), rgba(2, 6, 23, 0.76));
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 24px;
            padding: 1.25rem;
            box-shadow: 0 18px 42px rgba(2, 6, 23, 0.35);
            margin-bottom: 1rem;
        }

        .operation-title {
            color: #f8fafc;
            font-size: 1.2rem;
            font-weight: 950;
            margin-bottom: 0.3rem;
        }

        .operation-subtitle {
            color: #94a3b8;
            font-size: 0.94rem;
            line-height: 1.55;
            margin-bottom: 0.9rem;
        }

        .route-box {
            background: rgba(8, 47, 73, 0.44);
            border: 1px solid rgba(56, 189, 248, 0.28);
            border-left: 7px solid #38bdf8;
            border-radius: 20px;
            padding: 1.15rem;
            line-height: 1.7;
            box-shadow: 0 14px 34px rgba(2, 6, 23, 0.34);
            margin: 0.8rem 0 1rem 0;
        }

        .route-box-title {
            font-weight: 950;
            color: #f8fafc;
            margin-bottom: 0.55rem;
        }

        .route-box-text {
            color: #dbeafe;
            font-size: 0.98rem;
        }

        .status-ok {
            background: rgba(22, 101, 52, 0.28);
            border: 1px solid rgba(74, 222, 128, 0.25);
            color: #bbf7d0;
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            display: inline-block;
            font-weight: 850;
            font-size: 0.86rem;
        }

        .status-wait {
            background: rgba(113, 63, 18, 0.28);
            border: 1px solid rgba(251, 191, 36, 0.25);
            color: #fde68a;
            border-radius: 999px;
            padding: 0.35rem 0.75rem;
            display: inline-block;
            font-weight: 850;
            font-size: 0.86rem;
        }

        .info-note {
            background: rgba(30, 41, 59, 0.72);
            border: 1px solid rgba(148, 163, 184, 0.20);
            border-radius: 18px;
            padding: 1rem;
            color: #cbd5e1;
            line-height: 1.55;
            margin-bottom: 1rem;
        }

        .about-panel {
            background:
                linear-gradient(135deg, rgba(15, 23, 42, 0.94), rgba(8, 47, 73, 0.70));
            border: 1px solid rgba(125, 211, 252, 0.22);
            border-radius: 28px;
            padding: 1.7rem;
            box-shadow: 0 22px 52px rgba(2, 6, 23, 0.40);
        }

        .about-panel p {
            color: #cbd5e1;
            line-height: 1.7;
        }

        .dev-panel {
            background:
                linear-gradient(135deg, rgba(67, 20, 7, 0.74), rgba(15, 23, 42, 0.88));
            border: 1px solid rgba(251, 146, 60, 0.32);
            border-left: 8px solid #fb923c;
            border-radius: 24px;
            padding: 1.5rem;
            color: #fed7aa;
            font-weight: 850;
            box-shadow: 0 20px 48px rgba(2, 6, 23, 0.38);
        }

        /* ===============================
           MÉTRICAS
        =============================== */

        div[data-testid="stMetric"] {
            background: rgba(15, 23, 42, 0.86);
            border: 1px solid rgba(148, 163, 184, 0.22);
            border-radius: 18px;
            padding: 1rem;
            box-shadow: 0 14px 32px rgba(2, 6, 23, 0.30);
        }

        div[data-testid="stMetric"] label {
            color: #cbd5e1 !important;
            font-weight: 800;
        }

        div[data-testid="stMetricValue"] {
            color: #f8fafc !important;
        }

        /* ===============================
           TABELAS
        =============================== */

        [data-testid="stTable"] {
            border-radius: 18px;
            overflow: hidden;
            border: 1px solid rgba(148, 163, 184, 0.20);
            background: rgba(15, 23, 42, 0.80);
        }

        [data-testid="stTable"] table {
            color: #e5e7eb;
        }

        [data-testid="stTable"] thead tr th {
            background: #020617 !important;
            color: #f8fafc !important;
            font-weight: 900;
            border-color: rgba(148, 163, 184, 0.16) !important;
        }

        [data-testid="stTable"] tbody tr td,
        [data-testid="stTable"] tbody tr th {
            background: rgba(15, 23, 42, 0.94) !important;
            color: #e5e7eb !important;
            border-color: rgba(148, 163, 184, 0.14) !important;
        }

        /* ===============================
           EXPANDER
        =============================== */

        .streamlit-expanderHeader {
            background: rgba(15, 23, 42, 0.88);
            color: #f8fafc !important;
            border-radius: 14px;
            border: 1px solid rgba(148, 163, 184, 0.18);
            font-weight: 850;
        }

        .streamlit-expanderContent {
            background: rgba(2, 6, 23, 0.35);
            border: 1px solid rgba(148, 163, 184, 0.12);
            border-radius: 0 0 14px 14px;
        }

        [data-testid="stAlert"] {
            border-radius: 16px;
        }

        /* ===============================
           RESPONSIVO
        =============================== */

        @media (max-width: 900px) {
            .top-panel {
                grid-template-columns: 1fr;
            }

            .workflow {
                grid-template-columns: 1fr;
            }

            .mission-title {
                font-size: 2rem;
            }
        }
    </style>
    """, unsafe_allow_html=True)


carregar_estilos()


# =========================================================
# FUNÇÕES AUXILIARES DE INTERFACE
# =========================================================

def status_badge(condicao, texto_ok, texto_espera):
    if condicao:
        return f'<span class="status-ok">{texto_ok}</span>'
    return f'<span class="status-wait">{texto_espera}</span>'


def nomes_da_rota(rota, escolas):
    return " → ".join([escolas[i] for i in rota])


def rota_fixa_compativel(n):
    rota_base = [0, 1, 7, 2, 8, 3, 5, 6, 4, 0]

    if n == 9:
        return rota_base

    return gerar_solucao_inicial(n)


# =========================================================
# ESTADO DA APLICAÇÃO
# =========================================================

if "matriz" not in st.session_state:
    st.session_state.matriz = None

if "escolas" not in st.session_state:
    st.session_state.escolas = []

if "solucao_inicial" not in st.session_state:
    st.session_state.solucao_inicial = None

if "tipo_execucao_atual" not in st.session_state:
    st.session_state.tipo_execucao_atual = None

if "custo_inicial" not in st.session_state:
    st.session_state.custo_inicial = None


# =========================================================
# MENU LATERAL
# =========================================================

st.sidebar.markdown("## Cozinha Piloto")
st.sidebar.markdown(
    """
    <div class="info-note">
        Painel acadêmico para simulação de rotas de entrega usando heurísticas.
    </div>
    """,
    unsafe_allow_html=True
)

menu = st.sidebar.radio(
    "Menu principal",
    ["Métodos Básicos", "Algoritmos Genéticos", "Sobre"]
)

st.sidebar.markdown("---")

st.sidebar.markdown(
    status_badge(st.session_state.matriz is not None, "Problema gerado", "Problema pendente"),
    unsafe_allow_html=True
)

st.sidebar.markdown("<br>", unsafe_allow_html=True)

st.sidebar.markdown(
    status_badge(st.session_state.solucao_inicial is not None, "Solução inicial pronta", "Solução inicial pendente"),
    unsafe_allow_html=True
)


# =========================================================
# PÁGINA: MÉTODOS BÁSICOS
# =========================================================

if menu == "Métodos Básicos":

    st.markdown("""
    <div class="top-panel">
        <section class="mission-card">
            <div class="mission-kicker">Trabalho Prático — Módulo I</div>
            <div class="mission-title">Painel de Despacho Inteligente</div>
            <div class="mission-text">
                Sistema para simular e otimizar rotas de entrega da Cozinha Piloto
                para escolas de Cachoeira Paulista, usando métodos heurísticos aplicados
                ao Problema do Caixeiro Viajante.
            </div>
        </section>

        <aside class="identity-card">
            <div class="identity-label">Resumo da atividade</div>
            <div class="identity-row">
                <span>Problema</span>
                <strong>TSP</strong>
            </div>
            <div class="identity-row">
                <span>Contexto</span>
                <strong>Rotas escolares</strong>
            </div>
            <div class="identity-row">
                <span>Execuções</span>
                <strong>Fixo / Aleatório</strong>
            </div>
            <div class="identity-row">
                <span>Interface</span>
                <strong>Tema escuro</strong>
            </div>
        </aside>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="workflow">
        <div class="step-card">
            <div class="step-number">1</div>
            <div class="step-title">Configurar</div>
            <div class="step-desc">Escolha execução fixa ou aleatória.</div>
        </div>
        <div class="step-card">
            <div class="step-number">2</div>
            <div class="step-title">Gerar problema</div>
            <div class="step-desc">Crie a matriz de distâncias.</div>
        </div>
        <div class="step-card">
            <div class="step-number">3</div>
            <div class="step-title">Solução inicial</div>
            <div class="step-desc">Gere e avalie a rota inicial.</div>
        </div>
        <div class="step-card">
            <div class="step-number">4</div>
            <div class="step-title">Executar método</div>
            <div class="step-desc">Compare e visualize os resultados.</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # -----------------------------------------------------
    # ÁREA 1: CONFIGURAÇÃO
    # -----------------------------------------------------

    st.markdown("""
    <div class="operation-card">
        <div class="operation-title">1. Configuração da rota</div>
        <div class="operation-subtitle">
            Defina se o sistema usará uma matriz fixa da Cozinha Piloto ou uma instância aleatória.
        </div>
    </div>
    """, unsafe_allow_html=True)

    col_tipo, col_tamanho = st.columns([1, 1])

    with col_tipo:
        tipo_execucao = st.selectbox(
            "Tipo de Execução",
            ["FIXO", "ALEATÓRIO"],
            help="No modo FIXO, a matriz e a solução inicial são constantes. No modo ALEATÓRIO, o sistema gera os dados."
        )

    with col_tamanho:
        if tipo_execucao == "ALEATÓRIO":
            tamanho_problema = st.number_input(
                "Tamanho do Problema",
                min_value=3,
                value=6,
                step=1,
                help="Quantidade total de pontos, incluindo a Cozinha Piloto."
            )
        else:
            st.markdown("""
            <div class="info-note">
                <strong>Modo FIXO selecionado.</strong><br>
                Será usada uma matriz constante baseada no cenário da Cozinha Piloto.
            </div>
            """, unsafe_allow_html=True)

    col_gerar, col_solucao = st.columns(2)

    with col_gerar:
        gerar = st.button("Gerar Problema", use_container_width=True)

    with col_solucao:
        gerar_solucao = st.button("Gerar Solução Inicial", use_container_width=True)

    if gerar:
        if tipo_execucao == "FIXO":
            escolas, matriz = obter_problema_fixo()
        else:
            escolas, matriz = gerar_problema_aleatorio(tamanho_problema)

        st.session_state.escolas = escolas
        st.session_state.matriz = matriz
        st.session_state.solucao_inicial = None
        st.session_state.custo_inicial = None
        st.session_state.tipo_execucao_atual = tipo_execucao

        st.success("Problema gerado com sucesso.")

    if gerar_solucao:
        if st.session_state.matriz is None:
            st.error("Primeiro clique em 'Gerar Problema'.")
        else:
            n = len(st.session_state.escolas)

            if st.session_state.tipo_execucao_atual == "FIXO":
                rota = rota_fixa_compativel(n)
            else:
                rota = gerar_solucao_inicial(n)

            custo = avalia_rota(rota, st.session_state.matriz)

            st.session_state.solucao_inicial = rota
            st.session_state.custo_inicial = custo

            st.success("Solução inicial gerada e avaliada.")

    # -----------------------------------------------------
    # ÁREA 2: SITUAÇÃO DO PROBLEMA
    # -----------------------------------------------------

    if st.session_state.matriz is not None:
        st.markdown("---")
        st.markdown("## Painel do problema")

        col_m1, col_m2, col_m3, col_m4 = st.columns(4)

        with col_m1:
            st.metric("Pontos", len(st.session_state.escolas))

        with col_m2:
            st.metric("Execução", st.session_state.tipo_execucao_atual)

        with col_m3:
            st.metric("Origem", "Cozinha Piloto")

        with col_m4:
            if st.session_state.custo_inicial is not None:
                st.metric("Custo Inicial", f"{st.session_state.custo_inicial:.2f} km")
            else:
                st.metric("Custo Inicial", "Pendente")

        if st.session_state.solucao_inicial is not None:
            rota_inicial_texto = nomes_da_rota(
                st.session_state.solucao_inicial,
                st.session_state.escolas
            )

            st.markdown(f"""
            <div class="route-box">
                <div class="route-box-title">Rota inicial avaliada</div>
                <div class="route-box-text">{rota_inicial_texto}</div>
            </div>
            """, unsafe_allow_html=True)

        with st.expander("Visualizar matriz de distâncias", expanded=True):
            df_matriz = pd.DataFrame(
                st.session_state.matriz,
                columns=st.session_state.escolas,
                index=st.session_state.escolas
            )
            st.table(df_matriz)

    # -----------------------------------------------------
    # ÁREA 3: EXECUÇÃO DOS MÉTODOS
    # -----------------------------------------------------

    st.markdown("---")

    st.markdown("""
    <div class="operation-card">
        <div class="operation-title">2. Execução dos métodos heurísticos</div>
        <div class="operation-subtitle">
            Selecione o método, ajuste os parâmetros quando necessário e execute a busca.
        </div>
    </div>
    """, unsafe_allow_html=True)

    metodo = st.selectbox(
        "Método",
        [
            "Subida de Encosta",
            "Subida de Encosta com Tentativas",
            "Têmpera Simulada",
            "Análise Comparativa"
        ]
    )

    if metodo == "Subida de Encosta":
        st.markdown("""
        <div class="info-note">
            Método selecionado: <strong>Subida de Encosta</strong>.<br>
            Não há parâmetros adicionais para configurar.
        </div>
        """, unsafe_allow_html=True)

    elif metodo == "Subida de Encosta com Tentativas":
        tmax = st.number_input(
            "TMAX",
            min_value=1,
            value=10,
            help="Número máximo de tentativas sem melhora antes de encerrar."
        )

    elif metodo == "Têmpera Simulada":
        col_ti, col_tf, col_fr = st.columns(3)

        with col_ti:
            ti = st.number_input(
                "TI - Temperatura Inicial",
                value=100.0,
                step=10.0
            )

        with col_tf:
            tf = st.number_input(
                "TF - Temperatura Final",
                value=0.01,
                format="%.4f"
            )

        with col_fr:
            fr = st.number_input(
                "FR - Fator Redutor",
                value=0.90,
                min_value=0.01,
                max_value=0.99,
                step=0.01
            )

    elif metodo == "Análise Comparativa":
        st.markdown("""
        <div class="info-note">
            A análise comparativa executa automaticamente todas as configurações
            previstas na Tabela 1 da atividade.
        </div>
        """, unsafe_allow_html=True)

    executar = st.button("Executar Método", type="primary", use_container_width=True)

    if executar:
        if st.session_state.matriz is None:
            st.error("Gere o problema antes de executar um método.")
        elif st.session_state.solucao_inicial is None:
            st.error("Gere a solução inicial antes de executar um método.")
        else:
            rota_base = st.session_state.solucao_inicial
            matriz = st.session_state.matriz

            if metodo == "Subida de Encosta":
                melhor_rota, melhor_custo = subida_encosta(rota_base, matriz)

            elif metodo == "Subida de Encosta com Tentativas":
                melhor_rota, melhor_custo = subida_encosta_tentativas(
                    rota_base,
                    matriz,
                    tmax
                )

            elif metodo == "Têmpera Simulada":
                melhor_rota, melhor_custo = tempera_simulada(
                    rota_base,
                    matriz,
                    ti,
                    tf,
                    fr
                )

            elif metodo == "Análise Comparativa":
                st.markdown("## Tabela 1 — Análise Comparativa")

                with st.spinner("Executando análise comparativa..."):
                    n = len(st.session_state.escolas)
                    df_tabela = executar_analise(rota_base, matriz, n)

                st.table(df_tabela)

                st.markdown("""
                <div class="info-note">
                    <strong>SE:</strong> Subida de Encosta<br>
                    <strong>SET:</strong> Subida de Encosta com Tentativas<br>
                    <strong>TE:</strong> Têmpera Simulada
                </div>
                """, unsafe_allow_html=True)

                st.stop()

            st.markdown("---")
            st.markdown("## Resultado da execução")

            rota_final_texto = nomes_da_rota(
                melhor_rota,
                st.session_state.escolas
            )

            col_r1, col_r2, col_r3 = st.columns([1, 1, 1])

            with col_r1:
                st.metric("Método", metodo)

            with col_r2:
                st.metric("Distância Final", f"{melhor_custo:.2f} km")

            with col_r3:
                if st.session_state.custo_inicial is not None:
                    ganho = ((st.session_state.custo_inicial - melhor_custo) / st.session_state.custo_inicial) * 100
                    st.metric("Ganho", f"{ganho:.2f}%")
                else:
                    st.metric("Ganho", "Indisponível")

            st.markdown(f"""
            <div class="route-box">
                <div class="route-box-title">Melhor rota encontrada</div>
                <div class="route-box-text">{rota_final_texto}</div>
            </div>
            """, unsafe_allow_html=True)


# =========================================================
# PÁGINA: ALGORITMOS GENÉTICOS
# =========================================================

elif menu == "Algoritmos Genéticos":

    st.markdown("""
    <div class="top-panel">
        <section class="mission-card">
            <div class="mission-kicker">Módulo futuro</div>
            <div class="mission-title">Algoritmos Genéticos</div>
            <div class="mission-text">
                Esta área foi reservada para uma implementação futura de métodos evolutivos.
                Conforme solicitado na atividade, o sistema exibe apenas a indicação de desenvolvimento.
            </div>
        </section>

        <aside class="identity-card">
            <div class="identity-label">Estado do módulo</div>
            <div class="identity-row">
                <span>Status</span>
                <strong>Planejado</strong>
            </div>
            <div class="identity-row">
                <span>Uso atual</span>
                <strong>Indisponível</strong>
            </div>
        </aside>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="dev-panel">
        Módulo em desenvolvimento.
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# PÁGINA: SOBRE
# =========================================================

elif menu == "Sobre":

    st.markdown("""
    <div class="top-panel">
        <section class="mission-card">
            <div class="mission-kicker">Sobre a aplicação</div>
            <div class="mission-title">Cozinha Piloto e Otimização de Rotas</div>
            <div class="mission-text">
                Aplicação acadêmica desenvolvida para demonstrar o uso de métodos heurísticos
                em um problema de roteamento inspirado na entrega de alimentos para escolas.
            </div>
        </section>

        <aside class="identity-card">
            <div class="identity-label">Identificação</div>
            <div class="identity-row">
                <span>Discente</span>
                <strong>Luiz Francisco Charleaux</strong>
            </div>
            <div class="identity-row">
                <span>Discente</span>
                <strong>Caetano</strong>
            </div>
            <div class="identity-row">
                <span>Problema</span>
                <strong>Caixeiro Viajante</strong>
            </div>
        </aside>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="about-panel">
        <h2>Descrição do problema</h2>
        <p>
            O sistema trata o Problema do Caixeiro Viajante aplicado à otimização
            de rotas de entrega da Cozinha Piloto para escolas de Cachoeira Paulista.
        </p>

        <h2>Objetivo</h2>
        <p>
            Gerar uma rota inicial, avaliar seu custo e aplicar métodos heurísticos
            para buscar uma rota com menor distância total.
        </p>

        <h2>Métodos implementados</h2>
        <p>
            Subida de Encosta, Subida de Encosta com Tentativas, Têmpera Simulada
            e Análise Comparativa.
        </p>
    </div>
    """, unsafe_allow_html=True)