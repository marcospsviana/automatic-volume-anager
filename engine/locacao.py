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

    
    @staticmethod
    def locacao( nome, email, telefone, dia, hora, minuto, armario, language):
        
        __bk = Banco()
        __dia = dia
        __hora = hora
        __minuto = minuto
        print("locacao minuto", __minuto)
        __armario = str(armario)
        __nome = str(nome)
        __email = str(email)
        __telefone = str(telefone)
        __language = str(language)
        
        __get_armario = __bk.localisa_armario(__armario)
        if __get_armario == "nao ha armario disponivel" or __get_armario == []:
            return "armario da classe escolhida indisponível"
        
        else:
            result = __bk.locar_armario(__nome, __email, __telefone, __dia, __hora, __minuto, __armario, __language)
            return result
        
    @classmethod
    def finalizar_pagamento(self, senha):
        __bk = Banco()
        #__senha = senha
        #__nome = nome
        result = __bk.finalizar_pagamento(senha)
        return result
    
    """def send_email(self, nome, email, senha, compartimento, data_locacao, data_limite, hora_inicio_locacao, hora_fim_locacao, language):
        __bk = Banco()
        result = __bk.send_email(nome, email, senha, compartimento, data_locacao, data_limite, language)
        return result"""

            
    




if __name__ == "__main__":
    Locacao()
