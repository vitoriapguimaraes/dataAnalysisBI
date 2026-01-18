# 📊 Análise de Dados e Business Intelligence

> **Transformando dados brutos em decisões.**  
> Um portfólio interativo de Data Science e BI, reunindo análises exploratórias, dashboards estratégicos e testes estatísticos em uma única aplicação web.

<!--
![Demonstração do Sistema](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge&logo=appveyor)
-->

## 🎯 Objetivo

Centralizar diversos projetos de análise de dados em uma interface unificada, permitindo navegação fluida entre diferentes estudos de caso, desde churn de clientes até análises de mercado. O objetivo é demonstrar competências em:

- Limpeza e Tratamento de Dados (ETL)
- Análise Exploratória de Dados (EDA)
- Testes de Hipóteses e Estatística
- Visualização de Dados (Dataviz) e Storytelling
- Desenvolvimento de Data Apps com Streamlit

## 📂 Projetos e Funcionalidades

O repositório está organizado como um **Multi-Page App** com as seguintes análises principais:

- **💳 Análise de Cancelamento de Cartão (Churn)**
  - Diagnóstico completo de perfis de clientes propensos ao cancelamento.
  - Métricas de utilização, engajamento e dados demográficos.
  - Gráficos interativos (Plotly) para correlações e distribuições.

- **🛍️ Análise de Dados de Varejo**
  - Exploração de vendas e comportamento de compra.
  - Identificação de padrões sazonais e categorias de destaque.

- **🎧 Teste de Hipóteses Spotify**
  - Validação estatística sobre features musicais e popularidade.

- **🔄 Cancelamento de Assinaturas**
  - Estratégias de retenção baseadas em dados de serviços recorrentes.

- **🏠 Inside Airbnb**
  - Business Intelligence aplicado ao mercado de hospedagem e preços.

- **👥 Segmentação de Clientes (RFM)**
  - Clustering de consumidores baseado em Recência, Frequência e Valor.

## 🛠️ Tecnologias Utilizadas

- **Linguagem**: Python 3.12+
- **Framework Web**: Streamlit
- **Análise e Manipulação**: Pandas, NumPy, Scipy
- **Visualização**: Plotly Express, Matplotlib, Seaborn
- **Ferramentas**: VS Code, Git

## 🚀 Como Executar

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

## 📂 Estrutura de Diretórios

```
dataAnalysisBI/
├── data/                # Arquivos CSV e datasets brutos
├── notebooks/           # Scripts de EDA e experimentação
├── pages/               # Páginas individuais de cada análise
│   └── 1-Analise_de_Cancelamento_de_Clientes.py
├── utils/               # Módulos reutilizáveis
│   ├── load_file.py     # Carregamento otimizado de dados
│   ├── paths.py         # Gerenciamento de caminhos
│   ├── ui.py            # Componentes de UI (Sidebar)
│   └── visualizations.py # Biblioteca de gráficos padronizados
├── Painel.py            # Página Inicial (Home)
└── README.md            # Documentação do projeto
```

## 📊 Status

🛠️ Em manutenção

## 👩‍💻 Mais Sobre Mim

Acesse os arquivos disponíveis na [Pasta Documentos](https://github.com/vitoriapguimaraes/vitoriapguimaraes/tree/main/DOCUMENTOS) para mais informações sobre minhas qualificações e certificações.
