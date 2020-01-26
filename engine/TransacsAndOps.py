import sys, os
import datetime
import json
from time import sleep

class TransacsOps(object):
    def __init__(self, diretorio = os.getcwd()):
        self.diretorio = diretorio
    
    
    @classmethod
    def retorno_transacao(self):
        """ Esta função verifica o resultado da transação seja bem ou mal sucedida
        le o arquivo json que contem PWINFO_RESULTMSG a mensagem da transacao obtido da 
        biblioteca paygo 
        Entrada: Ausente 
        Retorno: type(json) PWINFO_RESULTMSG
        caso a transação não ocorra o arquivo é gravado com o valor da chave PWINFO_RESULTMSG str("SEM TRANSACAO")
        No caso de transacao efetuada é feita a leitura retorna PWINFO_RESULTMSG logo após é colocado um valor default
        para não interferir na proxima consulta, pois se na for setado a proxima consulta irá receber o valor de PWINFO_RESULTMSG
        da transacao anterior.
        """

        data = datetime.datetime.now()
        self.diretorio = os.getcwd()
        # LENDO O RETORNO DA TRANSACAO
        with open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(self.diretorio), 'r') as f:
            self.resultado_transacao = json.load(f)
        sleep(0.2)

        # FIM DE LEITURA DE RETORNO

        #SETANDO RETORNO PARA NÃO FICAR COM O ÚLTIMO DADO DE TRANSAÇÃO PARA A PROXIMA CONSULTA
        retorno = open('%s/engine/paygoWeb/comprovantes/retornotransacao.json'%(self.diretorio), 'w+')
        retorno.write('\n{  \n')
        retorno.write('     "DATA" : "%s %s %s %s %s",\n'%(data.day, data.month, data.year, data.hour, data.minute))
        retorno.write('     "PWINFO_RESULTMSG" : "SEM TRANSACAO"')
        retorno.write('\n}  \n')
        retorno.close()
        return self.resultado_transacao
    
    