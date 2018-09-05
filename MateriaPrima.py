from Banco import Banco
class MateriaPrima:

    def __init__(self, nome, materia, medida, preco, quant):
        self.nome = nome
        self.materia = materia
        self.medida = medida
        self.preco = preco
        self.quant = quant
        self.custoMateria = preco * quant
        self.insereBanco()

    def insereBanco(self):
        list = [self.nome, self.materia, self.medida, self.preco, self.quant, self.custoMateria]
        str = 'materiaprima (produto, descricao, unmedida, precounitario, quant, total)'

        Banco.insert(Banco, str, list)

    def relatorio(self):
        Banco.relatorio(Banco, 'materiaprima')