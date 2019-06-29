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
        __bk = Banco()
        __classe = classe
        __terminal = terminal
        __coluna = coluna
        __nivel = nivel
        __bk.cadastrar_armario(
            __classe, __terminal, __coluna, __nivel)

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
        __bk = Banco()
        __senha = senha
        __nome = nome
        result = __bk.liberar_armario(__senha, __nome)
        return result

