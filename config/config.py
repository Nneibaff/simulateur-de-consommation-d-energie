import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'ma_clé_secrète')  