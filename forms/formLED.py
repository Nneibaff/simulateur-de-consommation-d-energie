# formulaire avec wtforms

from wtforms import Form, IntegerField, SubmitField, FloatField, StringField, SelectField, FieldList, FormField
from wtforms.validators import InputRequired, NumberRange

import pandas as pd

# Charger les types de pièces du fichier CSV
def read_location_type():
    location_types_df = pd.read_csv('static/puissance_eclairage_type.csv')
    return location_types_df['Type de pièce'].tolist()

# Charger les types de luminaires du fichier CSV
def read_luminaire_type():
    power_types_df = pd.read_csv('static/puissance_eclairage_type.csv')
    return [power_types_df.columns[3], power_types_df.columns[5], power_types_df.columns[7]]

def read_trigger_system():
    trigger_system_df = pd.read_csv('static/trigger_system.csv')
    return trigger_system_df['trigger system'].tolist()



class HourForm(Form):
    hour = IntegerField('Hour', validators=[InputRequired(), NumberRange(min=0, max=23)]) 


# classe pour le formulaire de la page utilisateur
class FormLED(Form):
    project_name = StringField('Nom du projet', validators=[InputRequired()])
    location_type = SelectField('Type de lieu', choices=[(type, type) for type in read_location_type()], validators=[InputRequired()])
    luminaire_type = SelectField('Type de luminaires', choices=[(type, type) for type in read_luminaire_type()], validators=[InputRequired()])
    heuresutilisation = FieldList(FormField(HourForm), min_entries=1, max_entries=24)
    trigger_system = SelectField('Systeme de trigger', choices=[(type, type) for type in read_trigger_system()], validators=[InputRequired()])
    trigger_duration = IntegerField('Durée (en minutes)', validators=[NumberRange(min=1)], default=10)
    puissance = IntegerField('Puissance en W', default=60, validators=[InputRequired(), NumberRange(min=1, max=500)])
    nombreluminaire = IntegerField('Nombre de luminaires', default=1, validators=[InputRequired(), NumberRange(min=1, max=100)])
    contract_type = SelectField('Type de contrat', choices=[('fixe', 'Abonnement fixe'), ('heurescreusespleines', 'Abonnement heures creuses / heures pleines')], validators=[InputRequired()])
    prixheurescreuses = FloatField('Prix heures creuses', default=0)
    prixheurespleines = FloatField('Prix heures pleines', default=0)
    prixkWh = FloatField('Prix de kWh')
    submit = SubmitField('Calculer')
