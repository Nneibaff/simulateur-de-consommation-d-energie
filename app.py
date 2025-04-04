
# Importer les modules nécessaires
import os


# importer les modules pour les users
from uuid import uuid4
from functools import wraps


# importer les modules nécessaires pour flask
from flask import Flask, render_template, request

# importer le formumaire de la page utilisateur
from forms.formLED import FormLED

from config.config import Config
from config.firebase_config import db

# initialisation de l'application
app = Flask(__name__)
app.config.from_object(Config)
app.secret_key = os.urandom(24)  # code pour les sessions

# Importer les Blueprints
from routes.admin_routes import admin_bp
from routes.user_routes import user_bp
from routes.prices_routes import prices_bp

# from services.prices_fonctions import load_prices
# from services.calculs import calculer_consommation, generate_chart

# Importation des routes après l'init Firebase
app.register_blueprint(admin_bp, url_prefix='/admin')
app.register_blueprint(user_bp, url_prefix='/user')
app.register_blueprint(prices_bp, url_prefix='/prices')



# Page d'accueil avec formulaire
# Page d'accueil avec formulaire
# Page d'accueil avec formulaire

@app.route('/', methods=['GET', 'POST'])
def index():

    form = FormLED(request.form)

    consommation, consommation_led, economie, coût, coût_led, graph = None, None, None, None, None, None
    # prices = load_prices()
    total_heures_pleines, total_heures_creuses = 0, 0
    
    if request.method == 'POST': # and form.validate():
        puissance = form.puissance.data
        nombre = form.nombreluminaire.data
        prixkWh = float(request.form.get('prixkWh'))
        trigger_system = form.trigger_system.data
        trigger_duration = int(request.form.get('trigger_duration', 0))
        
        prixheurescreuses = request.form.get('prixheurescreuses')
        prixheurespleines = request.form.get('prixheurespleines')
        
        prixheurescreuses = float(prixheurescreuses) if prixheurescreuses else 0
        prixheurespleines = float(prixheurespleines) if prixheurespleines else 0
        
        heures_label = []
       
        for hour in range(24):
            heure = request.form.get(f'heuresutilisation_{hour}') 
            
            if heure:
                debut = int(heure.split("-")[0].strip().split(":")[0])
                fin = int(heure.split("-")[1].strip().split(":")[0])
                nuit_jour = "jour" if debut >= 6 and fin <= 21 else "nuit"
                heures_label.append(nuit_jour)
        total_heures_pleines = heures_label.count("jour")
        total_heures_creuses = heures_label.count("nuit")
        heures = total_heures_pleines + total_heures_creuses

        # Conditions à vérifier pour les valeurs saisies
        # if 1 <= puissance <= 500 and 1 <= nombre <= 100:
        #     consommation, consommation_led, economie, coût, coût_led = calculer_consommation(
        #         puissance, heures, nombre, prixkWh, trigger_system, trigger_duration, prixheurescreuses, prixheurespleines, total_heures_pleines, total_heures_creuses)
        #     graph = generate_chart(consommation, consommation_led, coût, coût_led)
        
        # if 'save_project' in request.form and 'user_uid' in session:
        #     user_uid = session['user_uid']
        #     user_ref = db.collection('users').document(user_uid)
        #     user_doc = user_ref.get()
        #     if user_doc.exists:
        #         project_name = form.project_name.data
        #         user_ref.collection('projects').add({
        #             'project_name': project_name,   
        #             'timestamp': datetime.now()
                # })
            
    return render_template("index.html",
                           form=form,
                           consommation=consommation,
                           consommation_led=consommation_led,
                           economie=economie,
                           coût=coût,
                           coût_led=coût_led,
                           graph=graph,
                        #    prices=prices,
                           total_heures_pleines=total_heures_pleines,
                           total_heures_creuses=total_heures_creuses)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)