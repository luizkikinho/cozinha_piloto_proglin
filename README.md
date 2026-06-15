PROJETO: OTIMIZAÇÃO DE ROTAS - COZINHA PILOTO

Discente: Luiz Francisco Charleaux e Caetano
Problema Tratado: Aplicação do Algoritmo do Caixeiro Viajante (TSP)
para otimização das rotas de entrega de alimentos da Cozinha Piloto
de Cachoeira Paulista.

O projeto foi desenvolvido em Python utilizando a biblioteca Streamlit
para a interface gráfica, seguindo o princípio de separação de
responsabilidades (Modularização).

O código-fonte está dividido em 6 arquivos principais:

1. app.py: Arquivo principal que gerencia a interface web, a navegação do topo (abas) e a interação com o usuário.
2. gerador_problema.py: Responsável por criar a matriz de distâncias (fixa ou aleatória) e gerar a solução inicial.
3. avalia_sucessor.py: Contém a função de avaliação de custo da rota e o motor de geração de vizinhos.
4. logica.py: Contém a implementação matemática dos algoritmos heurísticos de busca local (Subida de Encosta Clássica, Subida de Encosta com Tentativas e Têmpera Simulada).
5. analise_comparativa.py: Motor de automação que executa múltiplas baterias de testes com os algoritmos e gera os dados da "Tabela 1".
6. ag.py: Módulo responsável pela implementação do Algoritmo Genético, contendo a lógica de aptidão (Fitness), seleção por roleta, cruzamento de ordem (OX) e mutação (Swap).

Para rodar a aplicação em sua máquina local, siga os passos abaixo:

1. Certifique-se de ter o Python instalado (versão 3.8 ou superior).

2. Abra o terminal na pasta do projeto e instale as bibliotecas utilizadas:

   # Instala o framework da interface web, biblioteca matemática e de tabelas

   pip install streamlit numpy pandas

3. Após as instalações, inicie a aplicação com o comando:
   streamlit run app.py

4. O sistema abrirá automaticamente uma aba no seu navegador padrão (geralmente no endereço http://localhost:8501).

Guia de operação da interface:
O sistema possui uma navegação dividida em três seções: "Métodos Básicos", "Algoritmos Genéticos" e "Sobre".

ABA 1: MÉTODOS BÁSICOS
A) CONFIGURAÇÃO DO PROBLEMA: - Escolha entre "FIXO" ou "ALEATÓRIO". - No modo "FIXO", o sistema utiliza a matriz real da Cozinha Piloto. - Clique no botão "Gerar Problema" para criar a matriz de distâncias.

B) SOLUÇÃO INICIAL: - Clique no botão "Solução Inicial" para definir o ponto de partida e o custo inicial da rota base.

C) EXECUÇÃO DE ALGORITMOS: - Selecione o método desejado (Subida de Encosta, Subida de Encosta com Tentativas ou Têmpera Simulada). - Preencha os hiperparâmetros exigidos que aparecerão em tela (como TMAX ou Temperatura TI/TF). - Clique em "Executar" para ver o trajeto final e o novo custo reduzido.

D) ANÁLISE COMPARATIVA (TABELA 1): - Na seleção de método, escolha a opção "Análise Comparativa". - Clique em "Executar". O sistema calculará o Ganho percentual médio das baterias em todas as abordagens exigidas e exibirá em formato de tabela.

ABA 2: ALGORITMOS GENÉTICOS
E) EVOLUÇÃO DE POPULAÇÃO: - É obrigatório já ter gerado a matriz de problemas na aba de Métodos Básicos. - Defina os hiperparâmetros da evolução:
_ Tamanho da População (TP)
_ Número de Gerações (NG)
_ Taxa de Cruzamento (TC)
_ Taxa de Mutação (TM) - Clique em "Executar AG". O sistema aplicará os processos biológicos de cruzamento e mutação, retornando o melhor custo da última geração, além da sequência numérica e os locais percorridos.
