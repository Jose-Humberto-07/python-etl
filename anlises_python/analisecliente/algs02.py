from functools import reduce


### FUNCAO MAP ###

def portencia(x):
    return x ** 2


numeros = [1, 2, 3, 4, 5]


numeros_quadrado = map(lambda x : x * 5, numeros)



for i in numeros_quadrado:
    print(i)

print(list(numeros_quadrado))


def maiornumero(a, b):
    if a > b:
        return a
    else:
        return b

print("o maior número é :", maiornumero(10,11))
    


### FUNCAO REDUCE ###

numeros = [1, 2, 3, 4, 5]

def maiornumero(a, b):
    if (a > b):
        return a
    else:
        return b

print("o maior número é :", maiornumero(10,11))


numeros02 = [10, 20, 30, 40, 50]

func_maior_valor = lambda a,b : a if a > b else b

result = reduce(func_maior_valor, numeros02)

print(min(numeros02))
print(result)



