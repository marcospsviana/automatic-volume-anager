import sys
import os
from .data import Banco


class Armario(object):
    def __init__(self):
        __bk = Banco()    

    def cad_armario(classe, terminal, coluna, nivel):
        __bk = Banco()
        __classe = classe
        __terminal = terminal
        __coluna = coluna
        __nivel = nivel
        __bk.cadastrar_armario(
            __classe, __terminal, __coluna, __nivel)

    def remove_armario(id_armario):
        __bk
    
    def seleciona_armario(id_armario):
        
        __id_armario = id_armario
        
