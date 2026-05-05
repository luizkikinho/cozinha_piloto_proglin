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
    gerar_solucao_inicial
)

from avalia_sucessor import avalia_rota
from analise_comparativa import executar_analise

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="Trabalho Prático - Módulo I",
    page_icon="🚚",
    layout="wide"
)

# =========================================================
# ESTILO VISUAL (MATERIAL YOU / M3)
# =========================================================
def carregar_estilos():
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
        
        .stApp { background-color: #141218; color: #E6E1E5; font-family: 'Roboto', sans-serif; }
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}

        /* Tipografia Material 3 */
        .m3-headline { font-size: 2.25rem; font-weight: 400; color: #E6E1E5; line-height: 2.75rem; margin-bottom: 0.5rem; }
        .m3-title { font-size: 1.375rem; font-weight: 500; color: #E6E1E5; margin-bottom: 0.5rem; }
        .m3-body { color: #CAC4D0; font-size: 1rem; line-height: 1.5rem; font-weight: 400; }

        /* Botões */
        .stButton>button {
            border-radius: 100px; background-color: #4A4458; color: #E8DEF8; 
            border: none; font-weight: 500; min-height: 48px; width: 100%; transition: background-color 0.2s ease;
        }
        .stButton>button:hover { background-color: #635B70; color: #E8DEF8; }

        button[kind="primary"] { background-color: #D0BCFF !important; color: #381E72 !important; }
        button[kind="primary"]:hover { background-color: #E8DEF8 !important; }

        /* Inputs */
        div[data-baseweb="select"] > div, div[data-baseweb="input"] {
            background-color: #49454F; border-radius: 16px; border: none; color: #E6E1E5;
        }
        .stSelectbox label, .stNumberInput label { color: #E6E1E5 !important; font-weight: 500; }

        /* Blocos de Rota e Métricas */
        .m3-route-box {
            background-color: #36343B; border-radius: 16px; padding: 16px 24px; 
            color: #E6E1E5; margin-top: 12px; font-family: 'Roboto Mono', monospace; line-height: 1.6;
        }

        div[data-testid="stMetric"] { background-color: #2B2930; border-radius: 16px; padding: 16px; }
        div[data-testid="stMetric"] label { color: #CAC4D0 !important; font-weight: 500; }
        div[data-testid="stMetricValue"] { color: #D0BCFF !important; }

        /* Tabelas */
        [data-testid="stTable"] { background: transparent; }
        [data-testid="stTable"] th { background-color: #2B2930 !important; color: #E6E1E5 !important; border-bottom: 1px solid #49454F !important; }
        [data-testid="stTable"] td { background-color: #141218 !important; color: #CAC4D0 !important; border-bottom: 1px solid #2B2930 !important; }
        
        /* =======================================
           TOPBAR (Navegação Superior M3)
           ======================================= */
        [role="radiogroup"] {
            display: flex;
            flex-direction: row;
            justify-content: center;
            align-items: center;
            background-color: #1D1B20;
            padding: 8px;
            border-radius: 100px;
            gap: 8px;
            margin-bottom: 32px;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        }
        [role="radiogroup"] label {
            background-color: transparent !important;
            padding: 12px 24px !important;
            border-radius: 100px !important;
            margin: 0 !important;
            cursor: pointer;
            transition: background-color 0.2s ease;
        }
        [role="radiogroup"] label:hover {
            background-color: rgba(208, 188, 255, 0.08) !important;
        }
        [role="radiogroup"] label[data-checked="true"] {
            background-color: #4A4458 !important;
            color: #E8DEF8 !important;
        }
        [role="radiogroup"] label p {
            font-size: 1rem;
            font-weight: 500;
        }
    </style>
    """, unsafe_allow_html=True)

carregar_estilos()

# =========================================================
# FUNÇÕES AUXILIARES DE INTERFACE
# =========================================================
def nomes_da_rota(rota, escolas):
    return " ➔ ".join([escolas[i] for i in rota])

def rota_fixa_compativel(n):
    rota_base = [0, 1, 7, 2, 8, 3, 5, 6, 4, 0]
    return rota_base if n == 9 else gerar_solucao_inicial(n)

# =========================================================
# ESTADO DA APLICAÇÃO
# =========================================================
if "matriz" not in st.session_state:
    st.session_state.matriz = None
if "escolas" not in st.session_state:
    st.session_state.escolas = []
if "solucao_inicial" not in st.session_state:
    st.session_state.solucao_inicial = None
if "custo_inicial" not in st.session_state:
    st.session_state.custo_inicial = None

# =========================================================
# (1) TOPBAR DE NAVEGAÇÃO
# =========================================================
# Isso cria a barra horizontal no topo, substituindo a sidebar
menu = st.radio(
    "Navegação",
    ["Métodos Básicos", "Algoritmos Genéticos", "Sobre"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<hr style='border-color: transparent; margin: 0;'>", unsafe_allow_html=True)

# =========================================================
# (2) INTERFACE: MÉTODOS BÁSICOS
# =========================================================
if menu == "Métodos Básicos":

    st.markdown("<div class='m3-headline'>Métodos Básicos</div>", unsafe_allow_html=True)
    st.markdown("<div class='m3-body' style='margin-bottom: 2rem;'>Configuração e execução de heurísticas para o Problema do Caixeiro Viajante.</div>", unsafe_allow_html=True)

    # --- COMPONENTES DE CONFIGURAÇÃO ---
    st.markdown("<div class='m3-title'>Configuração do Problema</div>", unsafe_allow_html=True)
    
    col_tipo, col_tam = st.columns(2)
    with col_tipo:
        tipo_execucao = st.selectbox("Tipo de Execução", ["FIXO", "ALEATÓRIO"])
    
    with col_tam:
        if tipo_execucao == "ALEATÓRIO":
            tamanho_problema = st.number_input("Tamanho do Problema", min_value=3, value=6, step=1)
        else:
            tamanho_problema = None
            st.markdown("<div class='m3-body' style='margin-top: 32px;'>Tamanho predefinido pelo cenário fixo.</div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    # --- BOTÕES E EXIBIÇÃO DE GERAR PROBLEMA / SOLUÇÃO INICIAL ---
    col_btn_gerar, col_btn_sol = st.columns(2)
    with col_btn_gerar:
        if st.button("Gerar Problema"):
            if tipo_execucao == "FIXO":
                escolas, matriz = obter_problema_fixo()
            else:
                escolas, matriz = gerar_problema_aleatorio(tamanho_problema)
            
            st.session_state.escolas = escolas
            st.session_state.matriz = matriz
            st.session_state.solucao_inicial = None
            st.session_state.custo_inicial = None
            st.session_state.tipo_execucao = tipo_execucao

    with col_btn_sol:
        if st.button("Solução Inicial"):
            if st.session_state.matriz is not None:
                n = len(st.session_state.escolas)
                if st.session_state.get("tipo_execucao") == "FIXO":
                    rota = rota_fixa_compativel(n)
                else:
                    rota = gerar_solucao_inicial(n)
                
                custo = avalia_rota(rota, st.session_state.matriz)
                st.session_state.solucao_inicial = rota
                st.session_state.custo_inicial = custo
            else:
                st.warning("É necessário 'Gerar Problema' primeiro.")

    # --- ÁREAS DE EXIBIÇÃO ---
    if st.session_state.matriz is not None:
        st.markdown("<div class='m3-title' style='margin-top: 1.5rem;'>Matriz de Adjacências</div>", unsafe_allow_html=True)
        df_matriz = pd.DataFrame(st.session_state.matriz, columns=st.session_state.escolas, index=st.session_state.escolas)
        st.dataframe(df_matriz.style.format("{:.2f}"), use_container_width=True)

    if st.session_state.solucao_inicial is not None:
        st.markdown("<div class='m3-title' style='margin-top: 1.5rem;'>Solução Inicial e Avaliação</div>", unsafe_allow_html=True)
        col1, col2 = st.columns([1, 3])
        col1.metric("Custo (Distância)", f"{st.session_state.custo_inicial:.2f}")
        rota_str = nomes_da_rota(st.session_state.solucao_inicial, st.session_state.escolas)
        col2.markdown(f"<div class='m3-route-box' style='margin-top: 0;'>{rota_str}</div>", unsafe_allow_html=True)

    st.markdown("<hr style='border-color: #49454F; margin: 2rem 0;'>", unsafe_allow_html=True)

    # --- COMPONENTE DE SELEÇÃO DE MÉTODOS ---
    st.markdown("<div class='m3-title'>Execução de Heurísticas</div>", unsafe_allow_html=True)
    
    metodo = st.selectbox(
        "Selecione o Método",
        ["Subida de Encosta", "Subida de Encosta com Tentativas", "Têmpera Simulada", "Análise Comparativa"]
    )

    # Parâmetros dinâmicos de acordo com o método escolhido
    tmax, ti, tf, fr = None, None, None, None
    
    if metodo == "Subida de Encosta com Tentativas":
        tmax = st.number_input("TMAX", min_value=1, value=10)
    
    elif metodo == "Têmpera Simulada":
        c1, c2, c3 = st.columns(3)
        with c1: ti = st.number_input("TI", value=100.0)
        with c2: tf = st.number_input("TF", value=0.1)
        with c3: fr = st.number_input("FR", value=0.8)

    st.markdown("<br>", unsafe_allow_html=True)

    # --- BOTÃO EXECUTAR ---
    if st.button("Executar", type="primary"):
        if st.session_state.matriz is None or st.session_state.solucao_inicial is None:
            st.error("Gere o problema e a solução inicial primeiro.")
        else:
            rota_base = st.session_state.solucao_inicial
            matriz = st.session_state.matriz

            if metodo == "Análise Comparativa":
                st.markdown("<div class='m3-title' style='margin-top: 1.5rem;'>Tabela 1: Resumo da análise comparativa</div>", unsafe_allow_html=True)
                with st.spinner("Executando análise..."):
                    n = len(st.session_state.escolas)
                    df_tabela = executar_analise(rota_base, matriz, n)
                st.dataframe(df_tabela, use_container_width=True)
            
            else:
                with st.spinner(f"Executando {metodo}..."):
                    if metodo == "Subida de Encosta":
                        melhor_rota, melhor_custo = subida_encosta(rota_base, matriz)
                    elif metodo == "Subida de Encosta com Tentativas":
                        melhor_rota, melhor_custo = subida_encosta_tentativas(rota_base, matriz, tmax)
                    elif metodo == "Têmpera Simulada":
                        melhor_rota, melhor_custo = tempera_simulada(rota_base, matriz, ti, tf, fr)
                
                st.markdown("<div class='m3-title' style='margin-top: 1.5rem;'>Resultado da Execução</div>", unsafe_allow_html=True)
                col_res1, col_res2 = st.columns([1, 3])
                col_res1.metric(f"Novo Custo ({metodo})", f"{melhor_custo:.2f}")
                
                rota_final_texto = nomes_da_rota(melhor_rota, st.session_state.escolas)
                col_res2.markdown(f"<div class='m3-route-box' style='margin-top: 0;'>{rota_final_texto}</div>", unsafe_allow_html=True)

# =========================================================
# INTERFACE: ALGORITMOS GENÉTICOS
# =========================================================
elif menu == "Algoritmos Genéticos":
    st.markdown("<div class='m3-headline'>Algoritmos Genéticos</div>", unsafe_allow_html=True)
    st.info("Módulo em desenvolvimento.")

# =========================================================
# INTERFACE: SOBRE
# =========================================================
elif menu == "Sobre":
    st.markdown("<div class='m3-headline'>Sobre</div>", unsafe_allow_html=True)

    st.markdown("<div class='m3-title' style='margin-top: 1rem;'>Descrição do Problema</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='m3-body' style='margin-bottom: 2rem;'>
        O sistema trata da implementação de aplicações baseadas no clássico <strong>Problema do Caixeiro Viajante (TSP)</strong>. 
        Neste cenário específico, buscamos a otimização de rotas logísticas para distribuição de alimentos 
        saindo da Cozinha Piloto para diversas escolas no município de Cachoeira Paulista. O objetivo é encontrar 
        rotas (através de métodos heurísticos como Subida de Encosta e Têmpera Simulada) que minimizem a distância 
        total percorrida.
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='m3-title'>Discente(s)</div>", unsafe_allow_html=True)
    st.markdown("""
    <div class='m3-body'>
        <ul>
            <li>Luiz Francisco Charleaux e Caetano</li>
        </ul>
    </div>
    """, unsafe_allow_html=True)