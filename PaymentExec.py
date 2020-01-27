
from controllers import Management
from daemonize import Daemonize
import os, sys

pid = ("/tmp/payment.pid")
class PaymentTransac(object):
    def __init__(self, op):
        self.locacao = ''
        self.pagamento_ext = ''
        if "NOME" in args:
            self.locacao = self.args
        elif "SENHA" in args:
            self.pagamento_ext = self.args
    def efetuar_pagamento(self, locacao):
        self.window_payment.show()
        self.__armario = self.classe
        print("locacao", self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos)
        manager = Management()
        self.__result =  manager.locacao(self.__nome, self.__email, self.__telefone, self.__quantidade_diaria, self.__quantidade_horas, self.__quantidade_minutos, self.__armario, self.language, self.valor_total)
        count = 0
        #self.__result = self.__result[0]
        print("self.__result cadastro usuario ", self.__result[0])
        if self.__result[0][0] == "locacao concluida com sucesso":
            dia_inicio_locacao = self.__result[0][1]
            print("dia_inicio cadastro usuario", dia_inicio_locacao)
            hora_inicio_locacao = self.__result[0][2]
            print("hora_inicio cadastro usuario", hora_inicio_locacao)
            data_fim_locacao = self.__result[0][3]
            print("data_fim cadastro usuario", data_fim_locacao)
            hora_fim_locacao = self.__result[0][4]
            print("hora_fim cadastro usuario", hora_fim_locacao)
            self.senha = self.__result[0][5]
            print("__senha cadastro usuario", self.senha)
            compartimento = self.__result[0][6]
            print("compartimento cadastro usuario", compartimento)
            
        
            self.label_date_inicio_locacao.set_text(dia_inicio_locacao)
            self.label_date_fim_locacao.set_text(data_fim_locacao)
            self.label_hour_inicio_locacao.set_text(hora_inicio_locacao)
            self.label_hour_fim_locacao.set_text(hora_fim_locacao)
            self.label_senha.set_text(str(self.senha))
            self.label_compartimento.set_text(str(compartimento))
            
            #self.window_payment.hide()
            self.window_payment.hide()
            self.window_conclusao.show()
            
            
            self.id_armario = manager.localiza_id_armario(self.senha)
            retorno  = {
                "MESSAGE" : "SUCESSO",
                "RETORNO": self.id_armario
            }
            return retorno
        elif self.__result[0] == "armario da classe escolhida indisponível":
            return self.__result[0]
        else:
            return self.__result[0]
    
    def pagamento_extra(self, pagamento_ext):
        #self.window_payment.show()
        pagamento_extra = pagamento_ext
        resultado = Management.pagamento_extra(pagamento_extra["VALOR_TOTAL"], pagamento_extra["SENHA"])
        print(resultado)
        if "aprovada" in resultado:
            self.window_payment.hide()
            self.window_conclusao.show()

daemon = Daemonize(app="PaymentExec", pid = pid, action=PaymentTransac)
daemon.start()