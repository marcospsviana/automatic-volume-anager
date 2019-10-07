import datetime
from .data import Banco


class Cobranca(object):
    
    @staticmethod
    def cobranca( dia, hora, minuto):
        
        __bk = Banco()
        __result = ''
        data = datetime.datetime.now()
        __dia = int(dia)
        __hora = int(hora)
        __minuto = int(minuto)
        __total = (int(dia) * 24 * 60) + (int(hora) * 60  + __minuto)
        __futuro = data + \
            datetime.timedelta(
                days=__dia, hours=__hora, minutes=__minuto)
        __result = __bk.cobranca(__total, __futuro)
        print('modulo cobrança')
        return __result

    @staticmethod
    def pagamento(total, senha):
        __bk = Banco()
        __total = total
        print('******* total pagamento ********')
        print(__total)
        __result = __bk.pagamento(__total, senha)
        print('%------- pagamento ---------%')
        print(__result)
        if __result == "lk4thHG34=GKss0xndhe":
            return 'pagamento ok'
        else:
            return __result

    def finalizar( senha):
        def __init__(self):
            result = ''
            self.__bk = Banco()
            #self.__nome = nome
            self.__senha = senha
            result = self.__bk.finalizar(self.__senha)
            return result

if __name__ == "__main__":
    Cobranca()