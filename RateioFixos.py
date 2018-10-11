from Banco import Banco

class RateioFixos:
    def __init__(self, list):
        self.produto = list[0].text
        self.porc = list[1].text
        self.insereBanco()

    def insereBanco(self):
        list = [self.produto, self.porc]
        str = 'rateiocustosfixos (produto, porc)'
        prod = self.lista(RateioFixos, 'produto', ' WHERE produto="'+ self.produto +'"')
        if self.produto == prod:
            Banco.update(Banco, 'rateiocustosfixos', 'porc='+self.porc, ' WHERE produto="'+self.produto+'"')
        else:
            Banco.insert(Banco, str, list)

    def relatorio(self, col=None, cond=None):
        return Banco.relatorio(Banco, 'rateiocustosfixos', col, cond)

    def lista(self, table, col=None, cond=None):
        list = table.relatorio(table, col, cond)
        val = []
        if list is not None:
            for t in list:
                t = str(t).replace(",", "").replace(")", "").replace("(", "")
                val.append(t)
        return str(val)