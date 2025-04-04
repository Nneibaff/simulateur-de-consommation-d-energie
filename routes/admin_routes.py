from datetime import datetime
from forms.formAdmin import admin_login
from forms.formAdmin import new_admin
from flask import render_template, request, redirect, url_for, session, Blueprint
from werkzeug.security import generate_password_hash, check_password_hash
from uuid import uuid4
from config.firebase_config import db

admin_bp = Blueprint('admin', __name__)

# Route pour la page de connexion de l'admin
# Route pour la page de connexion de l'admin
# Route pour la page de connexion de l'admin

@admin_bp.route('/admin_login', methods=['GET', 'POST'])
def login():
    form = admin_login(request.form)
    if request.method == 'POST' and form.validate():
        uid_admin = str(uuid4())
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)

        # si la collection admin dans firestore n'existe pas, on l'a crée avec le premier admin en document
        if not db.collection('admins').get():
            db.collection('admins').document(uid_admin).set({
                'username': username,
                'password': hashed_password,
                'timescreate': datetime.now()
            })
            session['uid_admin'] = uid_admin
            return redirect(url_for('admin_home'))
        
        # on verifie si l'admin existe
        admins_ref = db.collection('admins')
        query = admins_ref.where('username', '==', username).stream()
        admin_doc = next(query, None)

        if admin_doc:
            admin = admin_doc.to_dict()
            stored_password_hash = admin.get('password')
            if check_password_hash(stored_password_hash, password):
                session['uid_admin'] = admin_doc.id
                return redirect(url_for('admin.admin_home'))
            
        return "Invalid credentials", 401
    return render_template('admin_login.html', form=form)

# Route pour la page d'accueil de l'admin
# Route pour la page d'accueil de l'admin
# Route pour la page d'accueil de l'admin

@admin_bp.route('/admin_home')
def admin_home():
    if 'uid_admin' not in session:
        return redirect(url_for('admin.login'))
    return render_template('admin_home.html')

# Route pour creer un nouvel admin
# Route pour creer un nouvel admin
# Route pour creer un nouvel admin

@admin_bp.route('/create_admin', methods=['GET', 'POST'])
def create_admin():
    if 'uid_admin' not in session:
        return redirect(url_for('login'))
    form = new_admin(request.form)
    if request.method == 'POST' and form.validate():
        uid_admin = str(uuid4())
        username = form.username.data
        password = form.password.data
        hashed_password = generate_password_hash(password)
        
        admins_ref = db.collection('admins')
        query = admins_ref.where('username', '==', username).stream()
        admin_doc = next(query, None)

        if admin_doc is None:
            db.collection('admins').document(uid_admin).set({
                'username': username,
                'password': hashed_password,
                'timescreate': datetime.now()
            })
            return redirect(url_for('admin_home'))
        return "Admin already exists", 400
    return render_template('create_admin.html', form=form)

# Route pour se deconnecter
# Route pour se deconnecter
# Route pour se deconnecter

@admin_bp.route('/logout')
def logout():
    session.pop('uid_admin', None)  # Remove the session
    return redirect(url_for('admin.login'))
