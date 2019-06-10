import sys, os
from data import Banco
import datetime
from datetime import date, timedelta


class Locacao(object):
    """ registra a locacao guardando uma senha , email e telefone de usuario a senha é ligada a locacao
        dados:
        nome, email, telefone, senha, armario: type( string )
        tempo_locado, dia, hora, minuto: type( int )
        total ( valor cobrado pela locacao): type ( float )
        tempo_corrido: type int ( tempo decorrido em que o armario ficou ocupado este 
        será utilizado caso o tempo tenha ultrapassado o limite de tempo contratado com 
        tolerancia de 10 minutos, o tempo restante será cobrado uma taxa extra sobre todo o excedente
        )
        data_locacao: type datetime, servirá como base de calculo para verificar se houve tempo excedente
        obtendo o tempo total em segundos da diferença de data_atual - data_locacao """


    def __init__(self):
        self.__bk = Banco()
        
    
    def locacao(self,  nome, email, telefone, dia, hora, minuto, armario):
        self.__data_locacao = datetime.datetime.now()
        self.__dia = int(dia)
        self.__hora = int(hora)
        self.__minuto = int(minuto)
        self.__armario = str(armario)
        self.__nome = str(nome)
        self.__email = str(email)
        self.__telefone = str(telefone)
        self.adiciona = date.fromordinal(self.__data_locacao.toordinal() + dia)
        self.__futuro = datetime.datetime(self.adiciona.year, self.adiciona.month, self.adiciona.day, self.__data_locacao.hour, self.__data_locacao.minute)
        self.__futuro = self.__futuro + timedelta(hours=self.__hora)
        self.__futuro = self.__futuro + timedelta(minutes=self.__minuto)
        self.__data_limite = self.__futuro#datetime.datetime(self.__futuro.year, self.__futuro.month, self.__futuro.day, self.__hora, self.__minuto, 0)
        
        
        self.__usr_id = self.__bk.select_user(self.__email, self.__telefone)
        #print('---- data e hora da locacao ------')
        #print(self.__hora_locacao)
        self.__get_armario = self.__bk.localisa_armario(self.__armario)
        if self.__get_armario == "nao ha armario disponivel":
            return "armario da classe escolhida indisponível"
        
        else:
            self.__bk.locar_armario(self.__nome, self.__email, self.__telefone, self.__data_limite, self.__armario)
            return "armario locado com sucesso"
        




if __name__ == "__main__":
    Locacao()
