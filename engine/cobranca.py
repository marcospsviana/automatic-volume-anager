from .DataAccessObjects import DataAccessObjectsManager as DAO
import datetime


class Cobranca(object):
    
    """@staticmethod
    def cobranca( dia, hora, minuto):
        
        __DAO = DAO()
        __result = ''
        data = datetime.datetime.now()
        __dia = int(dia)
        __hora = int(hora)
        __minuto = int(minuto)
        __total = (int(dia) * 24 * 60) + (int(hora) * 60  + __minuto)
        __futuro = data + \
            datetime.timedelta(
                days=__dia, hours=__hora, minutes=__minuto)
        __result = __DAO.cobranca(__total, __futuro)
        print('modulo cobrança')
        return __result"""

    @staticmethod
    def pagamento(total, senha):
        __DAO = DAO()
        __total = total
        print('******* total pagamento ********')
        print(__total)
        __result = __DAO.pagamento(__total, senha)
        print('%------- pagamento ---------%')
        print(__result)
        if 'aprovada' in __result.lower():
            return 'pagamento ok'
        else:
            return __result

    def finalizar( senha):
        def __init__(self):
            result = ''
            __DAO = DAO()
            #self.__nome = nome
            __senha = senha
            result = __DAO.finalizar(__senha)
            return result

if __name__ == "__main__":
    Cobranca()