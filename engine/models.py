from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Integer, String
from rasp import app
from config import SQLALCHEMY_DATABASE_URI


class Armario(db.Model):
    __tablename__ = 'tb_armarios'
    id_armario = db.Column('id_armario')
    classe = db.Column('classe')
    local = db.Column('local')
    terminal = db.Column('terminal')
    estado = db.Column('estado')
    coluna = db.Column('coluna')
    nivel = db.Column('nivel')


class Locacao(db.Model):
    __tablename__ = 'tb_locacao'
    id_locacao = db.Column('')
    data_locacao = db.Column('')
    tempo_locado = db.Column('')
    tempo_corrido = db.Column('')
    senha = db.Column('')
    id_armario = db.Column('')
    id_usuario = db.Column('')


class User(db.Model):
    __tablename__ = 'tb_usuario'
    id_usuario = db.Column('id_usuario', db.Integer, primary_key=True) 
    nome = db.Column('nome')
    email = db.Column('email')
    telefone = db.Column('telefone')
