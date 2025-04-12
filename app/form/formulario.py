"""
VALIDACIONES DE LOS DATOS DEL FORMULARIO
"""
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import StringField, SubmitField, DecimalField
from wtforms.validators import DataRequired, Email, Length
from wtforms.fields import DateField, TimeField, FileField

class Posiciones_form(FlaskForm):
    latitude = DecimalField("latitud", places=16, validators=[
        DataRequired(),
    ])
    longitude = DecimalField('longitud', places= 16, validators=[
        DataRequired(),
    ])
    name = StringField("nombre", validators=[
        DataRequired(),
        Length(max=50, min=3)
    ])
    date = DateField('Fecha', validators=[
        DataRequired()
    ])
    time = TimeField('Hora', validators=[
        DataRequired()
    ])
    file = FileField('File', validators=[
        FileRequired(),
    ])
    submit = SubmitField('Enviar')