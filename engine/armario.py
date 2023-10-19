import os
import sys

from .DataAccessObjects import DataAccessObjectsManager as DAO


class Armario:
    @classmethod
    def cad_armario(self, classe, terminal, coluna, nivel, porta, compartimento):

        __dao = DAO()
        __classe = classe
        __terminal = terminal
        __coluna = coluna
        __nivel = nivel
        __porta = porta
        __compartimento = compartimento
        result = __dao.cadastrar_armario(__classe, __terminal, __coluna, __nivel, __porta, __compartimento)
        return result

    @classmethod
    def fechar_armario(self, id_armario):
        __id_armario = id_armario
        __dao = DAO()
        result = __dao.fechar_armario(__id_armario)
        return result

    def seleciona_armario(id_armario):

        __id_armario = id_armario

    @staticmethod
    def seleciona_classe(classe):
        __dao = DAO()
        classe = classe
        __classe = __dao.seleciona_classe(classe)
        return __classe

    @staticmethod
    def listar_classes():
        __dao = DAO()
        classe = []
        classe = __dao.listar_classes_armarios()
        print('listar classe armario armario.py', classe)
        return classe

    @staticmethod
    def liberar_armario(senha):
        __dao = DAO()
        __senha = senha
        # __nome = nome
        result = __dao.liberar_armario(__senha)
        return result

    @staticmethod
    def finalizar(senha):
        result = ''
        # __nome = nome
        __senha = senha
        print('nome e senha de arm', __senha)
        __dao = DAO()
        result = __dao.finalizar(__senha)
        return result

    @staticmethod
    def abrir_armario(id_armario):
        result = ''
        # __nome = nome
        __id_armario = id_armario
        __dao = DAO()
        result = __dao.abrir_armario(__id_armario)
        print('result abrir armario em armario.py', result)
        return result

    @staticmethod
    def liberar_armario(id_armario):
        result = ''
        # __nome = nome
        __id_armario = id_armario
        __dao = DAO()
        result = __dao.liberar_armario(__id_armario)
        print('result abrir armario em armario.py', result)
        return result

    @staticmethod
    def localiza_id_armario(senha):
        __dao = DAO()
        __senha = senha
        print('senha em localiza id armario em armario.py', __senha)
        result = __dao.localiza_id_armario(__senha)
        return result
