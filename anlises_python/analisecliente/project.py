import pandas as pd



tabela = pd.read_csv("clientes.csv", encoding="latin", sep=";")

print(tabela)

tabela = tabela.drop("Unnamed: 8", axis=1)

print(tabela)


print(tabela.info())

print(tabela.describe())
print("Hello word")
print(tabela.count())
# valores no formato errado
tabela["Salário Anual (R$)"] = pd.to_numeric(tabela["Salário Anual (R$)"], errors="coerce")
print(tabela.info())
print(tabela["Salário Anual (R$)"])
print("soma de todos os salarios: ",tabela["Salário Anual (R$)"].sum())

# corrigir informações vazias
tabela = tabela.dropna()  # limpando linhas com valores vazios
print(tabela.info())
print(tabela.describe())



