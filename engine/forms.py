from flask_wtf import FlaskForm
from wtforms import Form, StringField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class FormTempo(FlaskForm):
    dia = IntegerField('Dia',validators=[DataRequired()])
    hora = IntegerField('Hora',validators=[DataRequired()])
    minuto = IntegerField('minuto',validators=[DataRequired()])
    nome = StringField('Nome', validators=[DataRequired()])
    email = StringField('E-mail', validators=[DataRequired()])
    telefone= StringField('Telefone', validators=[DataRequired()])
    submit = SubmitField('locar')