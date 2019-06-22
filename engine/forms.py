# -*- encoding: utf-8 -*-

from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, SubmitField, IntegerField, FloatField, SelectField, RadioField
from wtforms.validators import DataRequired


class FormTempo(Form):
    dia = IntegerField('Dia',validators=[DataRequired()])
    hora = IntegerField('Hora',validators=[DataRequired()])
    minuto = IntegerField('minuto',validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telefone= StringField('Telefone', validators=[DataRequired()])
    total = FloatField()
    submit = SubmitField('locar')
    confirma = RadioField('Confirma', choices=[('sim','sim'), ('não','não')])

class RecuperarBagagem(FlaskForm):
    nome = StringField('Telefone ou Email', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    senha = StringField('Senha', validators=[DataRequired()])
    submit = SubmitField('Recuperar Bagagem')



class CadArmario(Form):
    classe = SelectField('CLASSE', choices=[('A','A'),('B','B'),('C','C'),('D','D')])
    terminal = SelectField('TERMINAL', choices=[('1','1'),('2','2')])
    coluna = SelectField('COLUNA', choices=[('1','1'),('2','2')])
    nivel = SelectField('NÍVEL', choices=[('SUPERIOR','SUPERIOR'), ('INFERIOR', 'INFERIOR')])

