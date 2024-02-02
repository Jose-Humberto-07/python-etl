import pandas as pd



"""
# dataframe = pd.DataFrame()
venda = {'data': ['15/02/2021', '16/02/2021'],
         'valor': [500, 300],
         'produto': ['feijao', 'arroz'],
         'qtde': [50, 70],
        }
vendas_df = pd.DataFrame(venda)


print(vendas_df)
"""
vendas_df = pd.read_excel("Vendas.xlsx")
print(vendas_df)

print(vendas_df.head())
print(vendas_df.shape)
print(vendas_df.describe())

# pegar coluna
produtos = vendas_df[["Produto","ID Loja"]]
print(produtos)
print("############################################");
quantidade = vendas_df["Quantidade"]
print(quantidade)

# pegar uma linha
print(vendas_df.loc[1:5])
# pegar linhas que correspodem a uma condição
vendas_nortshopping_df = vendas_df.loc[vendas_df["ID Loja"] == "Norte Shopping"]
print(vendas_nortshopping_df)
vendas_riomar_df = vendas_df.loc[vendas_df["ID Loja"] == "Rio Mar Shopping Fortaleza"]
print(vendas_riomar_df)
# pegar várias linhas e colunas usando LOC
vendas_nortshopping_df = vendas_df.loc[vendas_df["ID Loja"] == "Norte Shopping", ["ID Loja", "Produto", "Quantidade"]]
print(vendas_nortshopping_df)

vendas_riomar_df = vendas_df.loc[vendas_df["ID Loja"] == "Rio Mar Shopping Fortaleza", ["ID Loja", "Produto", "Quantidade"]]
print(vendas_riomar_df)
print("total: ",vendas_riomar_df.count(), " maximo: ",vendas_riomar_df.max(), " minimo ",vendas_riomar_df.min())

# a partir de uma coluna que existe
vendas_df["Comissão"] = vendas_df["Valor Final"] * 0.05
print(vendas_df)
# criar uma coluna com valor padrão
vendas_df.loc[:, "Imposto"] = 0
print(vendas_df)

vendas_ribeirao_df = vendas_df.loc[vendas_df["ID Loja"] == "Ribeirão Shopping", ["ID Loja", "Produto", "Quantidade", "Comissão", "Imposto"]]
print(vendas_ribeirao_df)

#vendas_dezembro_df = pd.read_excel("/Vendas - Dez.xlsx")
#print(vendas_dezembro_df)



# Excluir linhas e colunas
#vendas_df = vendas_df.drop("Imposto", axis=1)


# deleter linhas e coluans completamente vazias
#vendas_df = vendas_df.dropna(how = "all", axis = 1)
#display(vendas_df)

# deletar linhas que possuem pelo menos 1 valor vazio
#vendas_df = vendas_df.dropna()
#display(vendas_df)

# preecher valores vazios
# preencher com a média da coluna
vendas_df["Comissão"] = vendas_df["Comissão"].fillna(vendas_df["Comissão"].mean())
print(vendas_df)

# preencher com o último valor
vendas_df = vendas_df.ffill()

# value counts
#transacoes_loja = vendas_df["ID Loja"].value_counts()
#display(transacoes_loja)

# group By
faturamento_produto = vendas_df[["Produto", "Valor Final"]].groupby("Produto").sum()
print(faturamento_produto)
faturamento_produto = vendas_df[["Produto", "Valor Final"]].groupby("Produto").mean()
print(faturamento_produto)