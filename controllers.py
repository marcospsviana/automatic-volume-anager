from engine.locacao import Locacao as loc
from engine.usuario import User as usr
class Management(object):
    ''' controllers: todos os controles de acesso nesta classe com funcoes de mesmo nome '''
    def locacao(self, nome, email, telefone, total, dia, hora, minuto, armario):
        ''' Obtem os dados do formulario de incricao de clientes e locacao dos armarios
            dados:
            nome, email, telefone, armario: string
            dia, hora, minuto, tempo_locado(total do tempo contratado em segundos): int'''
        self.__rec = ''
        self.__nome, self.__email, self.__telefone, self.__armario = nome, email, telefone, armario
        self.__total, self.__dia, self.__hora, self.__minuto = total, dia, hora, minuto
        self.__rec = self.cad_user(self.__nome, self.__email, self.__telefone)
        loc.locacao(self.__nome, self.__email, self.__telefone, self.__total, self.__dia, self.__hora, self.__minuto, self.__armario)

    def cad_user(self, nome, email, telefone):
        self.__nome = nome
        self.__email = email
        self.__telefone = telefone
        usr.create_usr(self.__nome, self.__email, self.__telefone)
    
    def cad_armarios(self, classe, local, terminal, nivel, coluna):
        
        self.__local = local
        self.__classe = classe
        self.__terminal = terminal
        self.__nivel = nivel
        self.__coluna = coluna
        
        




