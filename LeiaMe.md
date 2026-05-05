# Projeto: Otimização de Rotas — Cozinha Piloto

**Discente:** Luiz Francisco Charleaux e Caetano  
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
