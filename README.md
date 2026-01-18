# Análise de Dados e Business Intelligence

> **Transformando dados brutos em decisões.**  
> Um portfólio interativo de Data Science e BI, reunindo análises exploratórias, dashboards estratégicos e testes estatísticos em uma única aplicação web.

<!--
![Demonstração do Sistema](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge&logo=appveyor)
-->

## Objetivo

Centralizar diversos projetos de análise de dados em uma interface unificada, permitindo navegação fluida entre diferentes estudos de caso, desde churn de clientes até análises de mercado. O objetivo é demonstrar competências em:

- Limpeza e Tratamento de Dados (ETL)
- Análise Exploratória de Dados (EDA)
- Testes de Hipóteses e Estatística
- Visualização de Dados (Dataviz) e Storytelling
- Desenvolvimento de Data Apps com Streamlit

## Projetos e Funcionalidades

O repositório está organizado como um **Multi-Page App** com as seguintes análises principais:

| Módulo de Análise                    | Descrição e Funcionalidades                                                                        |
| :----------------------------------- | :------------------------------------------------------------------------------------------------- |
| **👥 Segmentação de Clientes (RFM)** | Clustering de consumidores baseado em Recência, Frequência e Valor (8 segmentos).                  |
| **🛍️ Dados de Varejo**               | Exploração de vendas, sazonalidade e comportamento de compra das operações de varejo.              |
| **💳 Cancelamento de Cartão**        | Diagnóstico de churn, métricas de engajamento e correlações com gráficos interativos.              |
| **🔄 Cancelamento de Assinaturas**   | Análise de churn em serviços de assinatura (Telco), com simulador de cenários e foco em contratos. |

## Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework Web**: Streamlit
- **Análise e Manipulação**: Pandas, NumPy, Scipy
- **Visualização**: Plotly Express, Matplotlib, Seaborn
- **Ferramentas**: VS Code, Git

## Como Executar

Siga os passos abaixo para rodar a aplicação localmente:

1. **Clone o repositório**

   ```bash
   git clone https://github.com/vitoriapguimaraes/dataScience.git
   cd dataScience/dataAnalysisBI
   ```

2. **Instale as dependências**
   Recomenda-se usar um ambiente virtual (`venv` ou `conda`).

   ```bash
   pip install -e .
   ```

   _Ou instale via requirements se disponível:_ `pip install -r requirements.txt`

3. **Execute a aplicação**

   ```bash
   streamlit run Painel.py
   ```

4. **Acesse no navegador**
   O app abrirá automaticamente em: `http://localhost:8501`

## Estrutura de Diretórios

```dash
dataAnalysisBI/
├── data/                # Arquivos CSV e datasets brutos
├── notebooks/           # Scripts de EDA e experimentação
├── pages/               # Páginas individuais de cada análise
│   ├── 1-Cancelamento_de_Clientes.py
│   ├── 2-Varejo.py
│   ├── 3-Segmentacao_RFM.py
│   └── 4-Cancelamento_de_Assinatura.py
├── utils/               # Módulos reutilizáveis
│   ├── load_file.py     # Carregamento otimizado de dados
│   ├── paths.py         # Gerenciamento de caminhos
│   ├── ui.py            # Componentes de UI (Sidebar)
│   └── visualizations.py # Biblioteca de gráficos padronizados
├── Painel.py            # Página Inicial (Home)
└── README.md            # Documentação do projeto
```

## Status

✅ Concluído

## Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
