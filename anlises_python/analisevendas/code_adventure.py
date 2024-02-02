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

# verificando as linhas vazinhas 
print(data.isna().sum())

# criando coluna de quantidade de dias de envio
data['Dias de Envio'] = data['Data Envio'] - data['Data Venda']

print(data)

# custo bruto do produto
data['Custo Total'] = data['Custo Unitário'] * data['Quantidade']

print(data)
# custo líquido do produto
data['% Lucro Bruto'] = ( 1 - ( data['Custo Total'] / data['Valor Venda'] ) ) * 100


print(data)