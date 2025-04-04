from datetime import datetime
from flask import render_template, request, redirect, url_for, session, Blueprint
from uuid import uuid4
from werkzeug.security import generate_password_hash, check_password_hash
from config.firebase_config import db
from forms.formUser import UserRegister
from forms.formUser import UserLogin


# from services.calculs import calculer_consommation
# from services.generate_graph import generate_chart
# from services.prices_fonctions import load_prices
from forms.formLED import FormLED




user_bp = Blueprint('user', __name__)

@user_bp.route('/create_user', methods=['GET', 'POST'])
def create_user():
    form = UserRegister(request.form)
    if request.method == 'POST' and form.validate():
        user_id = str(uuid4())
        email = form.email.data
        password = form.pwd.data
        nom = form.Nom.data
        prénom = form.Prénom.data
        hashed_password = generate_password_hash(password)
        
        users_ref = db.collection('users')

       # Vérifier si l'email existe déjà
        query = users_ref.where("email", "==", email).stream()
        if next(query, None):  # Si un utilisateur avec cet email existe déjà
            return "Email already exists", 400

        users_ref.document(user_id).set({
            'email': email,
            'mot de passe': hashed_password,
            'nom': nom,
            'prénom': prénom,
        })
        
        return redirect(url_for('user.login_user'))
    return render_template('create_user.html', form=form)


@user_bp.route('/user_login', methods=['GET', 'POST'])
def login_user():
    form = UserLogin(request.form)
    
    if request.method == 'POST' and form.validate():
        email = form.email.data
        password = form.pwd.data

        
        users_ref = db.collection("users")
        
        # vérifier si l'email existe dans la collection users
        query = users_ref.where("email", "==", email).stream()
        user_doc = next(query, None)
        
        if not user_doc:
            query = users_ref.where("uid", "==", email).stream()
            user_doc = next(query, None)
        
        if user_doc:
            user = user_doc.to_dict()
            hashed_password = user.get("mot de passe")
            if check_password_hash(hashed_password, password):
                session['user_uid'] = user_doc.id
                return redirect(url_for('user.user_home'))
        return "Invalid credentials", 401
   
    return render_template('user_login.html', form=form)


@user_bp.route('/user_home', methods=['GET', 'POST'])
def user_home():
    if 'user_uid' not in session:
        return redirect(url_for('user.login_user'))
    
    form = FormLED(request.form)
    # prices = load_prices()
    
    
    user_uid = session['user_uid']
    user_ref = db.collection('users').document(user_uid)
    user_doc = user_ref.get()
    projet_id = str(uuid4())
    simulation_id = str(uuid4())

    if not user_doc.exists:
        return "User not found", 404
    
    # Récupérer les données de l'utilisateur
    user_data = user_doc.to_dict()
    
    consommation, consommation_led, economie, coût, coût_led, graph = None, None, None, None, None, None
    total_heures_pleines, total_heures_creuses = 0, 0
    
    if request.method == 'POST':

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
        if 1 <= puissance <= 500 and 1 <= nombre <= 100:
            # consommation, consommation_led, economie, coût, coût_led = calculer_consommation(
            #     puissance, heures, nombre, prixkWh, trigger_system, trigger_duration, prixheurescreuses, prixheurespleines, total_heures_pleines, total_heures_creuses)
            # # appel de la fonction pour generer le graphique
            # graph = generate_chart(consommation, consommation_led, coût, coût_led)
            
            # enregistrer le projet avec l'uid de l'utilisateur

            project_ref = db.collection('projects').document(projet_id)
            project_ref.set({
                'project_name': form.project_name.data,
                'uid_user': user_uid,
                'timestamp': datetime.now()
             })


            simulation_ref = project_ref.collection('simulations').document(simulation_id)
            simulation_ref.set({
                'location_type': form.location_type.data,
                'luminaire_type': form.luminaire_type.data,
                'heuresutilisation': heures_label,
                'trigger_system': form.trigger_system.data,
                'trigger_duration': form.trigger_duration.data,
                'puissance': form.puissance.data,
                'nombreluminaire': form.nombreluminaire.data,
                'contract_type': form.contract_type.data,
                'prixheurescreuses': form.prixheurescreuses.data,
                'prixheurespleines': form.prixheurespleines.data,
                'prixkWh': form.prixkWh.data,
                'consommation': consommation,
                'consommation_led': consommation_led,
                'economie': economie,
                'coût': coût,
                'coût_led': coût_led,
                'total_heures_pleines': total_heures_pleines,
                'total_heures_creuses': total_heures_creuses,
                'graph': graph,
                })
    return render_template('user_home.html', form=form, user=user_data,
                           consommation=consommation, consommation_led=consommation_led,
                           economie=economie, coût=coût, coût_led=coût_led, graph=graph,
                           total_heures_pleines=total_heures_pleines, total_heures_creuses=total_heures_creuses)


@user_bp.route('/edit_info_user', methods=['GET', 'POST'])
def edit_info_user():
    if 'user_uid' not in session:
        return redirect(url_for('user.login_user'))
    
    
    user_uid = session['user_uid']
    user_ref = db.collection('users').document(user_uid)
    user_doc = user_ref.get()

    if not user_doc.exists:
        return "User not found", 404

    user_data = user_doc.to_dict()

    if request.method == 'POST':
        nom = request.form.get('nom')
        prénom = request.form.get('prénom')
        email = request.form.get('email')
        pwd = request.form.get('pwd')
        pwd2 = request.form.get('pwd2')


# si nouvelle email, verifier si elle n'existe pas déjà
        if email != user_data['email']:
            query = db.collection('users').where('email', '==', email).stream()
            if next(query, None):
                return "Email already exists", 400

        if pwd != pwd2:
            return "Passwords do not match", 400

        if pwd and pwd == pwd2:
            hashed_password = generate_password_hash(pwd)
            user_ref.update({
                'nom': nom,
                'prénom': prénom,
                'email': email,
                'mot de passe': hashed_password
            })
        else:
            user_ref.update({
                'nom': nom,
                'prénom': prénom,
                'email': email
            })
        return redirect(url_for('user.user_home'))

    return render_template('edit_info_user.html', user=user_data)

@user_bp.route('/saved_projects', methods=['GET', 'POST'])
def saved_projects():
    if 'user_uid' not in session:
        return redirect(url_for('user.login_user'))

    user_uid = session['user_uid']

    # Récupération des projets appartenant à l'utilisateur connecté
    projects_ref = db.collection('projects').where('uid_user', '==', user_uid)

    # Si une mise à jour est demandée via un formulaire POST
    if request.method == 'POST':
        project_id = request.form.get('project_id')
        
        if project_id:
            # Récupérer les champs du formulaire et s'assurer qu'ils ne sont pas None
            project_data = {key: request.form.get(key, '') for key in [
                'project_name', 'location_type', 'luminaire_type',
                'trigger_system', 'trigger_duration', 'puissance',
                'nombreluminaire', 'contract_type', 'prixheurescreuses',
                'prixheurespleines', 'prixkWh'
            ]}

            try:
                project_ref = db.collection('projects').document(project_id)
                project_ref.update(project_data)
                return redirect(url_for('user.saved_projects'))  # Redirection après mise à jour
            except Exception as e:
                print(f"Erreur lors de la mise à jour du projet {project_id}: {e}")

    # Récupération des projets de l'utilisateur
    projects = projects_ref.stream()
    projects_list = [{'id': project.id, **project.to_dict()} for project in projects]

    return render_template('saved_projects.html', projects=projects_list)

@user_bp.route('/logout_user')
def logout_user():
    session.pop('user_uid', None)
    return redirect(url_for('user.login_user'))