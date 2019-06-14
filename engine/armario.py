import sys, os
from .data import Banco

class Armario(object):
    def __init__(self):
        self.__bk = Banco()
    
    def cad_armario(self, classe, local, terminal):
		self.conn = mdb.connect(user='root', password='microat8051',database='coolbag')
		self.c = self.conn.cursor(buffered=True)
		self.classe = classe
		self.local = local
		self.terminal = terminal