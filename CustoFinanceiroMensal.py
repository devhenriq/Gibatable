from Banco import Banco
from Financeiro import Financeiro

class CustoFinanceiroMensal:
    def __init__(self, custo):
        self.invest = 0
        self.custo = 0
        self.custo = custo
        fin = Financeiro()
        self.invest = fin.balancoIni('emprestimos') + fin.balancoIni( 'capsocial')
        Banco.delete(Banco, 'custofinanceiro')
        self.insereBanco()

    def calculaTotal(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = 0
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val = val + float(t)
        return val


    def insereBanco(self):
        list = [self.custo, self.invest]
        str = 'custofinanceiro(custo, invest)'
        Banco.insert(Banco, str, list)



    def relatorio(self, col=None, cond=None):
        ret = Banco.relatorio(Banco, 'custofinanceiro', col, cond)
        return ret