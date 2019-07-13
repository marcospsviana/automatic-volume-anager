import sys
import os
from .data import Banco
from .locacao import Locacao


class Armario:
   

    def cad_armario(self, classe, terminal, coluna, nivel):
        
        self.__bk = Banco()
        self.__classe = classe
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        self.__bk.cadastrar_armario(
            self.__classe, self.__terminal, self.__coluna, self.__nivel)

    def remove_armario(id_armario):
        __bk = Banco()
    
    def seleciona_armario(id_armario):
        
        __id_armario = id_armario

    @staticmethod
    def listar_classes ():
        __bk = Banco()
        __classe = []
        __classe = __bk.listar_classes_armarios()
        return __classe
    
    @staticmethod
    def liberar_armario(senha, nome):
        __bk = Banco()
        __senha = senha
        __nome = nome
        result = __bk.liberar_armario(__senha, __nome)
        return result
    
    @staticmethod
    def finalizar(nome, senha):
        result = ''
        __nome = nome
        __senha = senha
        __bk = Banco()
        result = __bk.finalizar(__nome, __senha)
        return result
