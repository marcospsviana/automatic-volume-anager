import sys
import os
from .data import Banco
from .locacao import Locacao


class Armario:
   

    @classmethod
    def cad_armario(self, classe, terminal, coluna, nivel, porta, compartimento):
        
        __bk = Banco()
        __classe = classe
        __terminal = terminal
        __coluna = coluna
        __nivel = nivel
        __porta = porta
        __compartimento = compartimento
        result = __bk.cadastrar_armario(
            __classe, __terminal, __coluna, __nivel, __porta, __compartimento)
        return result

    @classmethod
    def fechar_armario(self, id_armario):
        __id_armario = id_armario
        __bk = Banco()
        result = __bk.fechar_armario(__id_armario)
        return result
    
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
    
    """@staticmethod
    def liberar_armario(senha):
        __bk = Banco()
        __senha = senha
        #__nome = nome
        result = __bk.liberar_armario(__senha)
        return result"""
    
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
    def abrir_armario(id_armario):
        result = ''
        #__nome = nome
        __id_armario = id_armario
        __bk = Banco()
        result = __bk.abrir_armario(__id_armario)
        return result
    
    @staticmethod
    def localiza_id_armario(senha):
        __bk = Banco()
        __senha = senha
        result = __bk.localiza_id_armario(__senha)
        return result

