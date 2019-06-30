import datetime
from .data import Banco


class Cobranca(object):
    
    def cobranca(dia, hora, minuto):
        def __init__(self):
            self.__bk = Banco()
            self.__result = ''
            data = datetime.datetime.now()
            self.__dia = int(dia)
            self.__hora = int(hora)
            self.__minuto = int(minuto)
            self.__total = (int(dia) * 24) + (int(hora) +
                                                int(dia)) * 3600 + self.__minuto
            self.__futuro = data + \
                datetime.timedelta(
                    days=self.__dia, hours=self.__hora, minutes=self.__minuto)
            self.__result = self.__bk.cobranca(self.__total, self.__futuro)
            return self.__result

    def pagamento(self, total):
        self.__bk = Banco()
        self.__total = total
        print('******* total pagamento ********')
        print(self.__total)
        result = self.__bk.cobranca_excedente(self.__total)
        print('%------- pagamento ---------%')
        print(result)
        if result == "armario liberado ":
            return 'pagamento ok'
        else:
            return result

    def finalizar(self, nome, senha):
        
        result = ''
        self.__bk = Banco()
        self.__nome = nome
        self.__senha = senha
        result = self.__bk.finalizar(self.__nome, self.__senha)
        return result

if __name__ == "__main__":
    Cobranca()