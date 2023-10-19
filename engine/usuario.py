from .DataAccessObjects import DataAccessObjectsManager as DAO


class User(object):
    __slots__ = ['__nome', '__email', '__telefone']

    def create_usr(nome, email, telefone):
        __DAO = DAO()
        __nome = nome
        __email = email
        __telefone = telefone
        __DAO.create_user(__nome, __email, __telefone)

    def select_usr(email, telefone):
        __DAO = DAO()
        __email = email
        __telefone = telefone
        result = __DAO.select_user(__email, __telefone)
        return result


if __name__ == '__main__':
    User()
