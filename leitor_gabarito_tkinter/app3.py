import pandas as pd

# Carregando o arquivo CSV
df = pd.read_csv("23M01E3AV2-2 - CENTRAL.txt", sep=";", header=None, names=["ra", "aluno", "question"])

# Dividindo os caracteres da coluna "question" em colunas separadas
df_letras = df["question"].apply(list).apply(pd.Series)
df_letras = df_letras.add_prefix('letra_')

# Concatenando os DataFrames
df = pd.concat([df, df_letras], axis=1)

# Exportando para Excel
df.to_excel("dados_com_colunas.xlsx", index=False)
