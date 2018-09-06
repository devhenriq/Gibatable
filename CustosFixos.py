from Banco import Banco
from Pessoa import Pessoa
from InvestimentoFixo import InvestimentoFixo

class CustosFixos:

    def __init__(self, limpeza, cont, mat, agua, aluguel, manutencao, outros):
        self.adm = 0
        self.dir = 0
        self.limpeza = limpeza
        self.cont = cont
        self.mat = mat
        self.agua = agua
        self.aluguel = aluguel
        self.manutencao = manutencao
        self.deprec = 0
        self.outros = outros
        self.calcula()

    def calcula(self):

        list = Pessoa.relatorio(Pessoa, "total", " WHERE categoria = 'Administrativo'")

        if list is not None:
            for t in list:
                t = str(t).replace(",","").replace(")","").replace("(","")
                self.adm = self.adm + float(t)

        list = Pessoa.relatorio(Pessoa, "total"," WHERE categoria = 'Diretor'")

        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")","").replace("(","")
                self.dir = self.dir + float(t)


        total = 0
        list = InvestimentoFixo.relatorio(InvestimentoFixo, "total", " WHERE categoria = 'Moveis e Utensilios' OR categoria = 'Maquinas e Equipamentos' OR categoria = 'Computadores/Equipamentos de Informatica' OR categoria = 'Fixos em Veiculos' OR categoria = 'Imoveis Predios' OR categoria = 'Imoveis Terrenos'")
        for dep in list:
            dep = str(dep).replace(",", "").replace(")","").replace("(","")
            total = total + float(dep)

        self.deprec = self.deprec + total
        print(self.deprec)

        Banco.delete(Banco, 'custosfixos')
        self.total = self.adm + self.dir + self.limpeza + self.cont + self.mat + self.agua + self.aluguel + self.manutencao + self.deprec + self.outros
        self.insereBanco()


    def insereBanco(self):
        list = [self.adm, self.dir, self.limpeza, self.cont, self.mat, self.agua, self.aluguel, self.manutencao, self.deprec, self.outros, self.total]
        str = 'custosfixos (maodeobra, prolabore, limpeza, contador, material, agua, aluguel, manutencao, deprec, outros, total)'

        Banco.insert(Banco, str, list)

    def relatorio(self, col = None, cond = None):
        ret = Banco.relatorio(Banco, 'custosfixos', col, cond)
        return ret