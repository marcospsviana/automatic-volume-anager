from raspcontrol.engine.data import LocArmario as loc
from raspcontrol.engine.data import Usuario as usr
class Management(object):
    ''' controllers: todos os controles de acesso nesta classe com funcoes de mesmo nome '''
    def locacao(self, nome, email, telefone, total, dia, hora, minuto, armario):
        ''' Obtem os dados do formulario de incricao de clientes e locacao dos armarios
            dados:
            nome, email, telefone, armario: string
            dia, hora, minuto: int'''
        self.nome, self.email, self.telefone, self.armario = nome, email, telefone, armario
        self.total, self.dia, self.hora, self.minuto = total, dia, hora, minuto
        usr.create_user(self.nome, self.email, self.telefone)
        loc.locar_armario(self.nome, self.email, self.telefone, self.dia, self.hora, self.minuto)



