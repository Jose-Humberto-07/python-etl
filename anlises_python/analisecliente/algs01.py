


def soma(a, b):
    return a + b

nota1 = 2
nota2 = 2
nota3 = 2
nota4 = 2


def mediaAluno(n1, n2, n3, n4):
    media = (n1 + n2 + n3 + n4) / 4

    if media >= 7 and media < 10:
       return "aprovado"
    
    if media <= 5 and media > 3:
       return "reprovado"
    if media <= 3 and media >= 0:
       return "Nota muito baixa"
    
result = mediaAluno(nota1, nota2, nota3, nota4)
    
print(result)


list = ["neymar", "messi", "cristiano ronaldo"]

for item in list:
   print(item)

print(list)

objeto = {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
}

print(objeto.keys())
print(objeto.values())


lista_objetos = [
    {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
},

 {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
},

 {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
},

 {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
},

 {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
},

 {
   "nome":"humberto",
   "idade":27,
   "altura": 1.74,
   "adress": {
      "cidade": "maracanau",
      "bairro": "jereissati",
      "rua": 44,
      "numero": 265,
      "pais": "Brasil"
   }
}
]


print(lista_objetos," ; ")

for item in lista_objetos:
   print(item)



qtd = 10
   
for i in range(qtd):
   print(i)


