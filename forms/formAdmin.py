# formulaire avec wtforms

from wtforms import Form, StringField, SubmitField, PasswordField
from wtforms.validators import InputRequired

class new_admin(Form):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = StringField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Créer')

class admin_login(Form):
    username = StringField('Nom d\'utilisateur', validators=[InputRequired()])
    password = PasswordField('Mot de passe', validators=[InputRequired()])
    submit = SubmitField('Se connecter')