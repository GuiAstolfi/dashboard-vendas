# Importando as bibliotecas que vou usar
import pandas as pd
import streamlit as st
import plotly.express as px

# Editando o layout do streamlit e dando um título
st.set_page_config(layout= 'wide')
st.header('📊 Dashboard de Análise de Vendas: Faturamento, Produtos e Performance por Loja')

# Carregando os dados com o pandas
df = pd.read_csv('dados_vendas.csv', sep=';', encoding='latin1')

# Mudando o nome das colunas para letras minúsculas para ficar mais fácil de manozear  
df.columns = df.columns.str.lower()

# Vendo as informações do DataFrame
df.info()

# Transformando a coluna data_venda em datetime, porque vimos em cima que ela não estava em datetime
df['data_venda'] = pd.to_datetime(df['data_venda'])

# Ordenando o DataFrame pela coluna de data_venda
df.sort_values('data_venda')

# Criando uma coluna mes com apenas o ano e o mês da coluna data_venda
df['mes'] = df['data_venda'].apply(lambda x: str(x.year) +'-'+ str(x.month))

# Dessa vez criando uma coluna apenas com o ano
df['year'] = df['data_venda'].apply(lambda x: str(x.year))

# Definindo as colunas que eu quero do DataFrame
df = df[['year', 'mes', 'estado', 'loja', 'produto', 'qtde', 'valor_unitario', 'valor_total', 'forma_pagamento']]

# Criando um botão de selecbox na sidebar
mes = st.sidebar.selectbox('**Escolha o Mês:**', df['mes'].unique())

# Apenas para ficar mais bonito
st.sidebar.write('---')

# Criando um DataFrame filtrado, para quando mudar o mês na sidebar, mude também no DataFrame
df_filtrado = df[df['mes'] == mes]

# Criando um DataFrame para as metricas da side bar, aqui estou agrupando meu DataFrame pelo mês e pela loja
# e somando o valor total
df_metrics = df.groupby(['mes', 'loja'])['valor_total'].sum().reset_index()

# Ordenando o DataFrame pela loja
df_metrics.sort_values('loja', inplace= True)

# Criando uma coluna de mês agrupando pela loja, somando pelo valor total e fazendo a porcentagem de MoM
# arredondando por 2 e preechendo valor miss por 0
df_metrics['mom'] = df_metrics.groupby('loja')['valor_total'].pct_change().mul(100).round(2).fillna(0)

# Aqui faço igual la em cima, para quando alguém mudar na sidebar o mês, mude também na análise MoM
df_metrics = df_metrics[df_metrics['mes'] == mes]

# Aqui estou fazendo um for para exibir as informaçôes na side bar
# A função "iterrows" ela retorna o indice( primeira variável) e a linha( segunda variável), aqui uso um "_" para ele nao exibir o indicie, apenas a linha,
# se eu não colocasse ele ia dar um erro
for _, row in df_metrics.iterrows():

    # Aqui estou pegando a linha da coluna loja e a linha da coluna  mom( da analise MoM )
    loja = row['loja']
    mom = row['mom']
    # Dentro do for estou fazendo um if que ele muda a cor e a figura quando os valores da coluna mom for maior, menor ou igual que
    if mom > 0:
        cor = 'normal'
        seta = '⬆️'
    elif mom < 0:
        cor = 'normal'
        seta = '⬇️'
    else:
        cor = 'off'
        seta = '➡️'
    # Aqui eu exibo as informações na sideabr
    st.sidebar.metric(
        # Faço um label que vai receber uma string formatada com o nome da loja que estiver na vez da variável
        label=f"Analise MoM - {loja}",

        # Aqui tenho o valor que também vai receber uma string formatada com a variável seta, e a variável mom
        # formatada para ter uma casa decimal atrás da virgula e ser um float
        value=f"{seta} {mom:.1f}%",

        # Aqui tenho um delya que também rece uma string e a variável mom formatada para ter uma casa decimal atrás da virgula,
        # esse delta ja vem com a setinha para baixo, para cima ou para o lado, a variável seta é com o emoji da seta,
        # apenas para ficar mais visível e mais bonito
        delta=f"{mom:.1f}%",

        # Temos aqui um delta cor, que vai receber a variável cor, que depende do resultado do if
        delta_color=cor
    )


with st.expander('**Faturamento Mensal e Preço dos Produtos por Loja. (Clique aqui)**'):
    col1, col2 = st.columns(2)
    with col1:
        st.write('### Faturamento Mensal por Estado e Loja')
        df_faturamento_mes = df_filtrado.groupby(['estado', 'loja'])['valor_total'].sum().reset_index()
        faturamento_total = df_faturamento_mes['valor_total'].sum()
        st.metric('Faturamento Mensal de todas lojas: ', f'R${faturamento_total:,.2f}')
        grafico1 = px.bar(df_faturamento_mes, x='estado', y='valor_total', text= 'valor_total', color='loja', color_discrete_sequence=['#e0f3f8','#abd9e9', '#74add1', '#4575b4', '#313695'])
        grafico1.update_traces(texttemplate='%{text:$,.0f}', textposition='outside')
        st.plotly_chart(grafico1)

    with col2:
        st.write('### Faturamento Mensal por Produto e Loja')
        loja = st.selectbox('**Escolha a Loja:**', df['loja'].unique())
        df_filtrado_produto = df.query('mes == @mes and loja == @loja')
        df_produtos = df_filtrado_produto.groupby(['loja', 'produto'])['valor_total'].sum().reset_index()
        grafico2 = px.bar(df_produtos, x='produto', y= 'valor_total', text= 'valor_total' ,color='loja')
        grafico2.update_traces(texttemplate='%{text:$,.0f}', textposition='outside')
        st.plotly_chart(grafico2)

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.write('### Análise Percentual de Faturamento Por Produto')
        df_agrupado = df_filtrado.groupby(['mes', 'loja', 'produto'])['valor_total'].sum().reset_index()
        df_agrupado['soma_total'] = df_agrupado.groupby(['loja'])['valor_total'].transform('sum')
        df_agrupado['percentual'] = (df_agrupado['valor_total'] / df_agrupado['soma_total']).mul(100).round(1)
        filter_loja = st.segmented_control('**Loja:**', df['loja'].unique())
        df_percentual = df_agrupado.query('mes == @mes and loja == @filter_loja')
        grafico3 = px.bar(df_percentual, x='produto', y='percentual', text='percentual', color='loja', color_discrete_sequence=['#fed976'])
        grafico3.update_traces(texttemplate= '%{text}%')
        st.plotly_chart(grafico3)

    with col2:
        st.write('### Quantidade de Produtos Vendidos por Loja')
        st.write('---')
        df_qtde = df_filtrado.groupby(['mes', 'loja'])['qtde'].sum().reset_index()
        grafico4 = px.bar(df_qtde, x='loja', y='qtde', text='qtde', color='loja', color_discrete_sequence=['#a1dab4', '#41b6c4', '#2c7fb8', '#253494', '#fed976'])
        st.plotly_chart(grafico4)