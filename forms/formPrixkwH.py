# formulaire avec wtforms

from wtforms import Form, StringField, FloatField, SubmitField
from wtforms.validators import InputRequired, NumberRange

class FormPrixkWh(Form):
    pays = StringField('Pays', validators=[InputRequired()])
    prix = StringField('Prix', validators=[InputRequired(), NumberRange(min=0)])
    devise = StringField('Devise', validators=[InputRequired()])
    submit = SubmitField('Ajouter')

