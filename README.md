# 📊 Dashboard de Análise de Vendas

## 🔗 Acesse o Dashboard

👉 [Clique aqui para acessar o dashboard](https://dashboard-loja.streamlit.app/)


Dashboard interativo construído com **Streamlit** e **Plotly** para análise de faturamento, produtos e performance por loja.

## 🖥️ Demonstração

O dashboard permite:
- Filtrar os dados por **mês** via sidebar
- Acompanhar a variação **MoM (Month-over-Month)** de faturamento por loja
- Analisar o **faturamento mensal por estado e loja**
- Comparar **faturamento por produto** em cada loja
- Visualizar a **participação percentual** de cada produto no faturamento
- Ver a **quantidade de produtos vendidos** por loja

## 📁 Estrutura do Projeto

```
dashboard-vendas/
│
├── dash.py              # Código principal do dashboard (Streamlit)
├── dados_vendas.csv     # Base de dados de vendas
├── requirements.txt     # Dependências do projeto
└── README.md            # Documentação do projeto
```

## 📦 Dependências

| Biblioteca   | Versão recomendada | Uso                          |
|--------------|--------------------|------------------------------|
| streamlit    | >= 1.32.0          | Interface do dashboard       |
| pandas       | >= 2.0.0           | Manipulação de dados         |
| plotly       | >= 5.20.0          | Gráficos interativos         |

## 📊 Sobre os Dados

O arquivo `dados_vendas.csv` contém registros de vendas com as seguintes colunas:

| Coluna           | Descrição                              |
|------------------|----------------------------------------|
| `DATA_VENDA`     | Data da venda                          |
| `PRODUTO`        | Nome do produto vendido                |
| `QTDE`           | Quantidade vendida                     |
| `VALOR_UNITARIO` | Preço unitário do produto              |
| `VALOR_TOTAL`    | Valor total da venda                   |
| `LOJA`           | Identificador da loja                  |
| `FORMA_PAGAMENTO`| Forma de pagamento utilizada           |
| `ESTADO`         | Estado onde a venda foi realizada      |

Os dados cobrem o período de **outubro a dezembro de 2023**, com vendas de 5 lojas nos estados SP, RJ, PR, SC e RS.

## 🛠️ Tecnologias Utilizadas

- [Python](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [Plotly Express](https://plotly.com/python/plotly-express/)
