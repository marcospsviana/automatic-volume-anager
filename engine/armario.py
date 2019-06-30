import sys
import os
from .data import Banco
from .locacao import Locacao


class Armario(object):
    def __init__(self):
        __bk = Banco()  
        TABELA_ENDERECAMENTO =   {
            "localizacao": '001',
            "classe":{
                "A": "01",
                "B": {"ESQUERDA": "02",
                "DIREITA": "03"},
                "C":[
                    {
                    "Q1":"04",
                    "Q2":"05",
                    "Q3":"06",
                    "Q4":"07",
                    }
                    ],
                "D":[
                    {

                    }
                ]
            }

        }

        

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
        def __init__(self):
            self.__bk = Banco()
            self.__classe = []
            self.__classe = self.__bk.listar_classes_armarios()
            return self.__classe
    
    def liberar_armario(senha, nome):
         def __init__(self):
            self.__bk = Banco()
            self.__senha = senha
            self.__nome = nome
            result = self.__bk.liberar_armario(self.__senha, self.__nome)
            return result

