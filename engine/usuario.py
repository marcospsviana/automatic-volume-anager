from .data import Banco

class User(object):        

    def create_usr(nome, email, telefone):
        __bk = Banco()
        __nome = nome
        __email = email
        __telefone = telefone
        __bk.create_user(__nome, __email, __telefone)
    def select_usr(email, telefone):
        __bk = Banco()
        __email = email
        __telefone = telefone
        result = __bk.select_user(__email, __telefone)
        return result




if __name__ == '__main__':
    User()