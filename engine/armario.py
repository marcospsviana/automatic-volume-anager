import sys
import os
from .data import Banco
from .locacao import Locacao


class Armario:
   

    @classmethod
    def cad_armario(self, classe, terminal, coluna, nivel):
        
        self.__bk = Banco()
        self.__classe = classe
        self.__terminal = terminal
        self.__coluna = coluna
        self.__nivel = nivel
        result = self.__bk.cadastrar_armario(
            self.__classe, self.__terminal, self.__coluna, self.__nivel)
        return result

    def remove_armario(id_armario):
        __bk = Banco()
    
    def seleciona_armario(id_armario):
        
        __id_armario = id_armario
    
    @staticmethod
    def seleciona_classe(classe):
        __bk = Banco()
        classe = classe
        __classe = __bk.seleciona_classe(classe)
        return __classe

    @staticmethod
    def listar_classes ():
        __bk = Banco()
        classe = []
        classe = __bk.listar_classes_armarios()
        print('listar classe armario armario.py', classe)
        return classe
    
    @staticmethod
    def liberar_armario(senha):
        __bk = Banco()
        __senha = senha
        #__nome = nome
        result = __bk.liberar_armario(__senha)
        return result
    
    @staticmethod
    def finalizar(senha):
        result = ''
        #__nome = nome
        __senha = senha
        print('nome e senha de arm', __senha)
        __bk = Banco()
        result = __bk.finalizar( __senha)
        return result
    
    @staticmethod
    def abrir_armario(senha):
        result = ''
        #__nome = nome
        __senha = senha
        __bk = Banco()
        result = __bk.abrir_armario(__senha, __nome)
        return result
