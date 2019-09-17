#!/usr/bin/python3
# -*- coding: utf-8 -*-

from engine.locacao import Locacao as loc
from engine.usuario import User as usr
from engine.armario import Armario as arm
from engine.cobranca import Cobranca as cb


class Management(object):
    ''' controllers: todos os controles de acesso nesta classe com funcoes de mesmo nome 
    Obtem os dados do formulario de incricao de clientes e locacao dos armarios
            dados:
            nome, email, telefone, armario: string
            dia, hora, minuto, tempo_locado(total do tempo contratado em segundos): int'''
    def locacao( self, nome, email, telefone, dia, hora, minuto, armario):
         
        self.__cobranca = ''
        self.__nome, self.__email, self.__telefone, self.__armario = nome, email, telefone, armario
        self.__dia, self.__hora, self.__minuto = dia, hora, minuto
        self.__rec = self.cad_user(self.__nome, self.__email, self.__telefone)
        result = loc.locacao(self.__nome, self.__email, self.__telefone, self.__dia, self.__hora, self.__minuto, self.__armario)
               
        return (result, self.__cobranca)

    def cad_user(self, nome, email, telefone):
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        usr.create_usr(self.__nome, self.__email, self.__telefone)
    
    def cad_armarios(self, classe, terminal, coluna, nivel):
        
        __classe = str(classe)
        __terminal = str(terminal)
        __nivel = str(nivel)
        __coluna = str(coluna)
        result = arm.cad_armario(__classe, __terminal, __coluna, __nivel)
        return result

    def remove_armarios(self, id_armario):
        __id = id_armario
        result = ''

    @staticmethod
    def lista_armarios():
        __classe = []
        __classe = arm.listar_classes()
        print('lista armarios controllers', __classe)
        return __classe
    def select_armario(self, armario):
        self.armario = armario
        __classe = arm.seleciona_classe(self.armario)
        return __classe


    @staticmethod
    def liberar_armarios(senha):
        #__nome = nome
        __senha = senha
        result = arm.liberar_armario(__senha, __nome)
        print('result controllers --->', result)
        return result
    def calculo(self, dia, hora, minuto):
        
        self.__dia = dia
        self.__hora = hora
        self.__minuto = minuto
        self.__cobranca =  cb.cobranca(self.__dia, self.__hora, self.__minuto)
        print('entrou em cobrança retorna total')
        return self.__cobranca

        
    def pagamento(self, total):
        self.__total  = total
        result = cb.pagamento(self, self.__total)
        return result
    
    def abre_armario(self, senha):
        result = ''
        __senha = senha
        
        result = arm.abrir_armario(__senha)
        print("result controllers--->", result)
        return result
    def finalizar(self, senha):
        result = ''
        #__nome = nome
        __senha = senha
        print('nome e senha de controllers', __senha)
        result = arm.finalizar(__senha)
        print("finalizar controllers--->", result)
        return result
    def finalizar_pagamento(self, senha):
        __senha = senha
        #__nome = nome
        result = loc.finalizar_pagamento(__senha)
        return result