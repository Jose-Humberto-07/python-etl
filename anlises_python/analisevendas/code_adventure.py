import pandas as pd
import numpy as np




# estraindo dados do excel
data = pd.read_excel('AdventureWorks.xlsx')

# dtviz
print(data)

# amostra dos dados
print(data.head())

print(data.columns)
# verificando as informacoes da base
print(data.info())

# tamanho da base
print(data.shape)

# verificando as linhas vazinhas 
print(data.isna().sum())

# criando coluna de quantidade de dias de envio
data['Dias de Envio'] = data['Data Envio'] - data['Data Venda']
print(data)

# custo bruto do produto
data['Custo Total'] = data['Custo Unitário'] * data['Quantidade']
print(data) 

# custo líquido do produto
data['Lucro Bruto'] = data['Valor Venda'] - data['Custo Total']
print(data)

# Lucro líquido da venda
data['Lucro Líquido'] = data['Lucro Bruto'] - data['Valor Desconto']
print(data)

# Percentual do Lucro bruto da venda
data['% Lucro Bruto'] = ( 1 - ( data['Custo Total'] / data['Valor Venda'] ) ) * 100
print(data)

# Percentual do Lucro líquido da venda
data['% Lucro Líquido'] = ( 1 - ( data['Custo Total'] / ( data['Valor Venda'] - data['Valor Desconto'] ) ) )*100


# contagem de venda por produto
print(data['Produto'].value_counts())

# Contagem de produtos vendidos
print(data.groupby('Produto')['Quantidade'].sum().sort_values(ascending=False))

# Lojas únicas
print(data['ID Loja'].unique())

# Quantidade de lojas únicas
print(len(data['ID Loja'].unique()))

# Menor data no conjuto de dados
print(data['Data Venda'].min())

# Maior data no conjuto de dados
print(data['Data Venda'].max())

# Agrupamento dos valores médios por produtos
valores = ['Produto', 'Valor Desconto', 'Valor Venda', 
           'Custo Total', 'Lucro Bruto', 'Lucro Líquido',
           '% Lucro Bruto', '% Lucro Líquido']
print(data[valores].groupby(['Produto']).mean())

# Somando os valores totais
total_descontos = data['Valor Desconto'].sum()
total_vendas = data['Valor Venda'].sum()
total_custos = data['Custo Total'].sum()
total_lucro_bruto = data['Lucro Bruto'].sum()
total_lucro_liquido = data['Lucro Líquido'].sum()

# Usando a função currency da biblioteca locale para formatar o valor
import locale
locale.setlocale(locale.LC_MONETARY, 'en_US.UTF-8')
# Mostrando os valores totais
print('Total de descontos foi ---->',locale.currency(total_descontos))
print('Total de vendas foi ------->',locale.currency(total_vendas))
print('Total de custos foi ------->',locale.currency(total_custos))
print('Lucro bruto foi ----------->',locale.currency(total_lucro_bruto))
print('Lucro líquido foi --------->',locale.currency(total_lucro_liquido))