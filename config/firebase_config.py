import os
import firebase_admin
from firebase_admin import credentials, firestore

# Initialisation de la connexion à Firestore
CURR_DIR: str = os.path.dirname(__file__)
cred = credentials.Certificate(os.path.join(os.path.dirname(CURR_DIR), "config", "firestore-creds.json"))
firebase_admin.initialize_app(cred)
db = firestore.client()