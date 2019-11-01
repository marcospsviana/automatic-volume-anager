from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Integer, String
from rasp import app
from config import SQLALCHEMY_DATABASE_URI
db = SQLAlchemy(app)

class Armario(db.Model):
    __tablename__ = 'tb_armarios'
    id_armario = db.Column('id_armario')
    classe = db.Column('classe')
    local = db.Column('local')
    terminal = db.Column('terminal')
    estado = db.Column('estado')
    coluna = db.Column('coluna')
    nivel = db.Column('nivel')
    def __init__(self, classe, local, terminal, estado, coluna, nivel):
        self.classe = classe
        self.local = local
        self.terminal = terminal
        self.estado = estado
        self.coluna = coluna
        self.nivel = nivel



class Locacao(db.Model):
    """ registra a locacao guardando uma senha , email e telefone de usuario a senha é ligada a locacao
        dados:
        nome, email, telefone, senha, armario: type( string )
        tempo_locado, dia, hora, minuto: type( int )
        total ( valor cobrado pela locacao): type ( float )
        tempo_corrido: type int ( tempo decorrido em que o armario ficou ocupado este 
        será utilizado caso o tempo tenha ultrapassado o limite de tempo contratado com 
        tolerancia de 10 minutos, o tempo restante será cobrado uma taxa extra sobre todo o excedente
        )
        data_locacao: type datetime, servirá como base de calculo para verificar se houve tempo excedente
        obtendo o tempo total em segundos da diferença de data_atual - data_locacao """

    __tablename__ = 'tb_locacao'
    id_locacao = db.Column('')
    data_locacao = db.Column('data_locacao')
    tempo_locado = db.Column('tempo_locado')
    tempo_corrido = db.Column('tempo_corrido')
    senha = db.Column('senha')
    id_armario = db.Column('id_armario')
    id_usuario = db.Column('id_usuario')
    def __init__(self, data_locacao, tempo_locado, tempo_corrido, senha, id_armario, id_usuario ):
        self.data_locacao = data_locacao
        self.tempo_locado = tempo_locado
        self.tempo_corrido = tempo_corrido
        self.senha = senha
        self.id_armario = id_armario
        self.id_usuario = id_usuario
    def locacao( nome, email, telefone, dia, hora, minuto, armario):
        def __init__(self):
            self.__dia = int(dia)
            self.__hora = int(hora)
            self.__minuto = int(minuto)
            self.__armario = str(armario)
            self.__nome = str(nome)
            self.__email = str(email)
            self.__telefone = str(telefone)
            
            self.__get_armario = Locacao.query.filter_by(self.__armario).first()#self.__bk.localisa_armario(self.__armario)
            if self.__get_armario == "nao ha armario disponivel" or self.__get_armario == [] or self.__get_armario == None:
                return "armario da classe escolhida indisponível"
            
            else:
                self.__bk.locar_armario(self.__nome, self.__email, self.__telefone, self.__dia, self.__hora, self.__minuto, self.__armario)
                return "armario locado com sucesso"


class User(db.Model):
    __tablename__ = 'tb_usuario'
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True) 
    nome = db.Column('nome')
    email = db.Column('email')
    telefone = db.Column('telefone')
    def __init__(self, nome, email, telefone):
        self.nome = nome
        self.email = email
        self.telefone = telefone
