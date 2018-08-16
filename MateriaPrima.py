class MateriaPrima:

    def __init__(self, nome, materia, medida, preco, quant):
        self.nome = nome
        self.materia = materia
        self.medida = medida
        self.preco = preco
        self.quant = quant
        self.custoMateria = preco * quant

    def insereBanco(self):
        print