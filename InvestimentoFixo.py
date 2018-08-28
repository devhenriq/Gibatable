import Banco

class InvestimentoFixo:

    def __init__(self, descricao, quant, valorUnit, categoria):
        self.descr = descricao
        self.quant = quant
        self.valorUnit = valorUnit
        self.valorTotal = valorUnit * quant
        self.categoria = categoria
        self.insereBanco()

    def insereBanco(self):
        conn = Banco.connect()
        cur = conn.cursor()

        cur.execute("""
                INSERT INTO investimentofixo (descricao, quant, valorunitario, total, categoria) 
                VALUES (?,?,?,?,?)
                """, (self.descricao, self.quant, self.valorUnit, self.valorTotal, self.categoria))

        cur.commit()
        conn.close()
