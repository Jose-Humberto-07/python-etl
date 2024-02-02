import pandas as pd


# ANALISANDO A BASE
vendas_df = pd.read_excel("Vendas.xlsx")
print(vendas_df)
print(vendas_df.head())
print(vendas_df.shape)
print(vendas_df.describe())
print(vendas_df.info())


print("estrutura da base: ", vendas_df.shape)

print(vendas_df.loc[vendas_df["ID Loja"] == "Norte Shopping"])


print("###################################################################################")
print(vendas_df.loc[vendas_df["ID Loja"] == "Norte Shopping", ["Produto"]].head())
print(vendas_df.head(10))








