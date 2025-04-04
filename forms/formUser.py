from wtforms import Form, StringField, PasswordField, EmailField
from wtforms.validators import DataRequired, Length, EqualTo, Email

class UserRegister(Form):
  email = EmailField("Email", validators=[DataRequired(), Email()])
  pwd = PasswordField("Mot de passe", validators=[DataRequired()])
  pwd2 = PasswordField("Confirmer mot de passe", validators=[DataRequired(), EqualTo("pwd")])
  Nom = StringField("Nom", validators=[DataRequired(), Length(min=2, max=10)])
  Prénom = StringField("Prénom", validators=[DataRequired(), Length(min=2, max=10)])
  

class UserLogin(Form):
  email = StringField("Votre email", validators=[DataRequired()])
  pwd = PasswordField("mot de passe", validators=[DataRequired()])