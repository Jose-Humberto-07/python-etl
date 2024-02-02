# IMPORTANDO BIBLIOTECAS
import pandas as pd

# ANALISANDO A BASE
vendas_df = pd.read_excel("Vendas.xlsx")
print(vendas_df)
print(vendas_df.head())
print(vendas_df.shape)
print(vendas_df.describe())
print(vendas_df.info())


# pegar coluna

produtos = vendas_df[["ID Loja", "Produto"]]
print(produtos)
print("teste")

print("#####################################")

# quantidade de vendas
quantidade_de_vendas = vendas_df["Quantidade"]
print(quantidade_de_vendas)

# quantidade de vendas por loja
quantidade_vendas_loja = vendas_df[["ID Loja", "Quantidade"]]
print(quantidade_vendas_loja)

# pegar uma linha
print(vendas_df.loc[1:10])

# total, media, maximo, minimo da loja riomar
vendas_riomar = vendas_df.loc[vendas_df["ID Loja"] == "Rio Mar Shopping Fortaleza", ["ID Loja", "Produto", "Quantidade"]]
print("total: ", vendas_riomar.count(), " máximo: ", vendas_riomar.max(), " mínimo: ", vendas_riomar.min())