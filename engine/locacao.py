# -*- encoding: utf-8 -*-
import sys, os
from .data import Banco
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

    
    def locacao( nome, email, telefone, dia, hora, minuto, armario):
        __bk = Banco()
        __dia = int(dia)
        __hora = int(hora)
        __minuto = int(minuto)
        __armario = str(armario)
        __nome = str(nome)
        __email = str(email)
        __telefone = str(telefone)
        
        #__usr_id = __bk.select_user(__email, __telefone)
        #print('---- data e hora da locacao ------')
        #print(__hora_locacao)
        __get_armario = __bk.localisa_armario(__armario)
        if __get_armario == "nao ha armario disponivel" or __get_armario == []:
            return "armario da classe escolhida indisponível"
        
        else:
            __bk.locar_armario(__nome, __email, __telefone, __dia, __hora, __minuto, __armario)
            return "armario locado com sucesso"
        




if __name__ == "__main__":
    Locacao()
