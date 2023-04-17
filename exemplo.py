
class Pessoa:
    def __init__(self , nome:str , idade:int ):
        self.nome = nome
        self.idade = idade


pessoa1 = Pessoa("Roberto",29)

print( pessoa1.nome )