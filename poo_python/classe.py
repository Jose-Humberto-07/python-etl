class Pessoa:
    def __init__(self, nome, idade):
        self.nome = nome
        self.idade = idade
        
    def __str__(self) -> str:
        return self.nome
        


    def setNome(self, nome):
        self.nome = nome

    def getNome(self):
        return self.nome



pessoa1 = Pessoa("humberto", 27)


pessoa1.setNome("Neymar")
pessoa1.nome = "teste"

# print(pessoa1.idade, pessoa1.nome)
print(pessoa1)

print("encapsulamento: ", pessoa1.getNome())