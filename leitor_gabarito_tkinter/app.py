import pandas as pd

base = pd.read_csv('23M01E3AV2-2 - CENTRAL.txt', sep=';', names=['ra', 'aluno', 'question'])

listateste = []
cont = 1
for cont in range(91):
    listateste.append(cont)
    cont += cont


print("LISTATESTE: ", listateste)

base.columns([f'coluna_{i+1}' for i in range(len(listateste))])

print(base['question'].str.len())

print(base['question'].str.split(''))






#base.to_excel('test2.xlsx', index=False)
print(base)



"""
teste = open("23M01E3AV2-2 - CENTRAL.txt")
print("python")
print(teste.read())
"""