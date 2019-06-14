import sys
import os
from .data import Banco


class Armario(object):
        

    def cad_armario(classe, terminal, coluna, nivel):
        __bk = Banco()
        __classe = classe
        __terminal = terminal
        __coluna = coluna
        __nivel = nivel
        __bk.cadastrar_armario(
            __classe, __terminal, __coluna, __nivel)
