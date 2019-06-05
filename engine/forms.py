from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, SubmitField, IntegerField, FloatField
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

class RecuperarBagagem(FlaskForm):
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    senha = StringField('Senha', validators=[DataRequired()])

class RecupererBagages(FlaskForm): #récupérer bagages
    nom = StringField('Nom', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    telephone = StringField('Téléphone', validators=[DataRequired()])
