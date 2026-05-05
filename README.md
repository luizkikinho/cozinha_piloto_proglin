# Projeto: Otimização de Rotas — Cozinha Piloto

**Discentes:** Luiz Francisco Charleaux e Caetano  
**Problema tratado:** Aplicação do Algoritmo do Caixeiro Viajante (TSP) para otimização das rotas de entrega de alimentos da Cozinha Piloto de Cachoeira Paulista.

## Descrição do Projeto

O projeto foi desenvolvido em **Python**, utilizando a biblioteca **Streamlit** para a interface gráfica, seguindo o princípio de separação de responsabilidades por meio da **modularização**.

O código-fonte está dividido em **5 arquivos principais**:

1. **`app.py`**  
   Arquivo principal que gerencia a interface web, os menus e a interação com o usuário.

2. **`gerador_problema.py`**  
   Responsável por criar a matriz de distâncias, seja fixa ou aleatória, e gerar a solução inicial, respeitando a regra de roteamento fixo quando exigido.

3. **`avalia_sucessor.py`**  
   Contém a função de avaliação de custo da rota e o motor de geração de vizinhos, também chamado de sucessor, garantindo a integridade dos pontos de origem e destino, que representam a Cozinha Piloto.

4. **`logica.py`**  
   Contém a implementação matemática pura dos algoritmos heurísticos de busca:
   - Subida de Encosta Clássica;
   - Subida de Encosta com Tentativas;
   - Têmpera Simulada.

5. **`analise_comparativa.py`**  
   Motor de automação que executa múltiplas baterias de testes com os algoritmos e gera os dados da **Tabela 1**, calculando a porcentagem de ganho de cada método.

---

## Como Rodar a Aplicação

Para executar a aplicação em sua máquina local, siga os passos abaixo.

### 1. Verifique a instalação do Python

Certifique-se de ter o **Python 3.8 ou superior** instalado em sua máquina.

### 2. Instale as bibliotecas necessárias

Abra o terminal na pasta do projeto e instale as bibliotecas individualmente:

```bash
# Instala o framework da interface web
pip install streamlit

# Instala a biblioteca para cálculos matemáticos e matrizes
pip install numpy

# Instala a biblioteca para geração e manipulação de tabelas
pip install pandas
```

### 3. Execute a aplicação

Após as instalações, inicie a aplicação com o comando:

```bash
streamlit run app.py
```

### 4. Acesse no navegador

O sistema abrirá automaticamente uma aba no navegador padrão.

Caso isso não aconteça, acesse manualmente:

```txt
http://localhost:8501
```

---

## Guia de Operação da Interface

Para realizar um teste completo, siga a sequência abaixo.

### A) Configuração do Problema

1. No menu lateral, escolha entre **FIXO** ou **ALEATÓRIO**.
2. No modo **FIXO**, o sistema utiliza a matriz real da Cozinha Piloto.
3. No modo **ALEATÓRIO**, é possível definir a quantidade de escolas para o teste.
4. Clique no botão **GERAR PROBLEMA** para criar a matriz de distâncias.

### B) Solução Inicial

1. Clique no botão **SOLUÇÃO INICIAL** para definir o ponto de partida.
2. No modo **FIXO**, a solução inicial é constante, conforme exigido pela atividade.
3. No modo **ALEATÓRIO**, a solução inicial é gerada de forma randômica.

### C) Execução de Algoritmos

1. No campo **Selecione o Método**, escolha o algoritmo desejado:
   - **SE** — Subida de Encosta;
   - **SET** — Subida de Encosta com Tentativas;
   - **TE** — Têmpera Simulada.

2. Caso escolha **SET** ou **TE**, campos adicionais para parâmetros, como **TMAX** ou **Temperatura**, aparecerão automaticamente.

3. Clique em **EXECUTAR MÉTODO** para visualizar:
   - A melhor rota encontrada;
   - A distância final;
   - O desempenho do método selecionado.

### D) Análise Comparativa — Tabela 1

1. Selecione a opção **Análise Comparativa**.
2. Clique em **EXECUTAR MÉTODO**.
3. O sistema executará automaticamente todas as **11 configurações exigidas na atividade**.
4. O resultado será exibido em uma tabela comparativa com o cálculo do **ganho percentual** de cada método.

---

## Estrutura Geral do Projeto

```txt
projeto/
│
├── app.py
├── gerador_problema.py
├── avalia_sucessor.py
├── logica.py
└── analise_comparativa.py
```

---

## Tecnologias Utilizadas

- **Python 3.8+**
- **Streamlit**
- **NumPy**
- **Pandas**

---

## Objetivo

O objetivo do projeto é aplicar algoritmos heurísticos para resolver uma variação do problema do **Caixeiro Viajante**, buscando otimizar rotas de entrega de alimentos realizadas pela Cozinha Piloto de Cachoeira Paulista.
