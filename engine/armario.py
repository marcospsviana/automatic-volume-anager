import sys
import os
from .data import Banco
from .locacao import Locacao


class Armario:
   

    def cad_armario(classe, terminal, coluna, nivel):
        def __init__(self):
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
    
    def liberar_armario(senha, nome):
         def __init__(self):
            self.__bk = Banco()
            self.__senha = senha
            self.__nome = nome
            result = self.__bk.liberar_armario(self.__senha, self.__nome)
            return result

